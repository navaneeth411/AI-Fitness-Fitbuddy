from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles

from .database import get_db, User
from .gemini_service import generate_workout, generate_nutrition_tip, update_plan


app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")
app.mount("/static",
StaticFiles(directory="app/static"),
name="static")

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/generate-workout", response_class=HTMLResponse)
def generate(
    request: Request,
    user_id: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    weight: str = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(
        User.user_id == user_id
    ).first()

    plan = generate_workout(
        name,
        age,
        weight,
        goal,
        intensity
    )

    tip = generate_nutrition_tip(goal)

    if existing:
        existing.name = name
        existing.age = age
        existing.weight = weight
        existing.goal = goal
        existing.intensity = intensity
        existing.original_plan = plan
        existing.updated_plan = None
        existing.nutrition_tip = tip

        user = existing

    else:
        user = User(
            user_id=user_id,
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
            original_plan=plan,
            nutrition_tip=tip
        )

        db.add(user)

    db.commit()
    db.refresh(user)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user": user,
            "plan": user.original_plan,
            "tip": user.nutrition_tip,
            "updated": False
        }
    )


@app.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if not user:
        return templates.TemplateResponse(
            "message.html",
            {
                "request": request,
                "message": "User ID not found. Please generate a plan first."
            }
        )

    revised = update_plan(
        user.original_plan,
        feedback,
        user.goal,
        user.intensity
    )

    user.updated_plan = revised

    user.nutrition_tip = generate_nutrition_tip(
        user.goal
    )

    db.commit()
    db.refresh(user)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "user": user,
            "plan": user.updated_plan,
            "tip": user.nutrition_tip,
            "updated": True
        }
    )


@app.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(
    request: Request,
    db: Session = Depends(get_db)
):
    users = db.query(User).order_by(
        User.id.desc()
    ).all()

    return templates.TemplateResponse(
        "all_users.html",
        {
            "request": request,
            "users": users
        }
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "project": "FitBuddy AI Fitness"
    }

