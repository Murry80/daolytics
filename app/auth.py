# auth.py
from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from urllib.parse import urlencode

from .models import User
from .database import get_db
from .core.security import hash_password, verify_password

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

# Signup page
@router.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": "Email already exists"}
        )
    
    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Redirect to login page with success message
    query_params = urlencode({"success": "Account created successfully! Please log in."})
    return RedirectResponse(f"/login?{query_params}", status_code=status.HTTP_302_FOUND)


# Login page
@router.get("/login")
def login_page(request: Request, success: str = None, error: str = None):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "success": success,
            "error": error
        }
    )

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"}
        )
    
    # Simple session cookie placeholder
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="user_id", value=str(user.id))
    return response


# Logout
@router.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("user_id")
    return response


