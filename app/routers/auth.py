from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.utils.security import create_access_token
from app.database import get_db
from app.utils.templates import render_template
from app.services.auth_service import authenticate_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None):
    return render_template(
        "login.html",
        {
            "request": request,
            "error": error,
            "app_name": "Restoran Otomasyon Sistemi"
        }
    )


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, username, password)

    if not user:
        return RedirectResponse(
            url="/auth/login?error=Kullanıcı adı veya şifre hatalı",
            status_code=303
        )

    # JWT token oluştur
    access_token = create_access_token(
        data={"sub": user.username}
    )

    response = RedirectResponse(
        url="/dashboard/",
        status_code=303
    )

    # Cookie'ye token yaz
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True
    )

    return response


@router.get("/logout")
async def logout():

    response = RedirectResponse(
        url="/auth/login",
        status_code=303
    )

    response.delete_cookie("access_token")

    return response