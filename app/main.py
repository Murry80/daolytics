from fastapi import FastAPI, Request, UploadFile, File, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import shutil, os
from .models import User, File as FileModel
from .auth import router as auth_router
from .process_csv import analyze_trades
from .database import Base, engine, SessionLocal

# Initialize DB and ensure uploads folder exists
Base.metadata.create_all(bind=engine)
os.makedirs("uploads", exist_ok=True)

# App setup
app = FastAPI()
app.include_router(auth_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Home route
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("index.html", {"request": request, "users": users})

# CSV upload route
@app.post("/upload", response_class=HTMLResponse)
async def upload_csv(
    request: Request,
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = os.path.join("uploads", file.filename)

    # Save uploaded file
    contents = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    # Analyze trades
    result = analyze_trades(file_path, user_id)

    # Save file record to DB
    new_file = FileModel(user_id=user_id, filename=file.filename, result_path=result['chart'])
    db.add(new_file)
    db.commit()

    # Render results page
    return templates.TemplateResponse("results.html", {"request": request, "result": result})
