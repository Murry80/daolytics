from fastapi import FastAPI, UploadFile, File, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from database import Base, engine, SessionLocal
from models import User, File
from auth import router as auth_router
from process_csv import analyze_trades
from sqlalchemy.orm import Session
import shutil, os

# Initialize DB
Base.metadata.create_all(bind=engine)

# App setup
app = FastAPI()
app.include_router(auth_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
def upload_csv(request: Request, user_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    result = analyze_trades(file_path, user_id)
    
    # Save file record to DB
    new_file = File(user_id=user_id, filename=file.filename, result_path=result['chart'])
    db.add(new_file)
    db.commit()
    
    return templates.TemplateResponse("results.html", {"request": request, "result": result})
