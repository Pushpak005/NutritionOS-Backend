from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import text
from app.database import engine
from app.utils.nutrition_score import (
    calculate_score,
    recommendation_reason
)
from app.utils.goal_match import (
    calculate_goal_match,
    goal_match_label
)
from app.utils.badge_engine import generate_badges
from app.utils.explanation_engine import generate_explanation
from app.utils.ranking_engine import calculate_final_score
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.recommendations import router as recommendations_router
from app.routers.meal_logs import router as meal_log_router
from app.routers.profile import router as profile_router
from app.routers.nutrition import router as nutrition_router
from app.routers.restaurants import router as restaurant_router
from app.routers.meals import router as meals_router
from app.routers.my_meals import router as my_meals_router
from app.routers.dashboard import router as dashboard_router
from app.routers.ai import router as ai_router
from app.routers.analytics import router as analytics_router
from app.routers.score import router as score_router






app = FastAPI(title="NutritionOS API")
from fastapi.middleware.cors import CORSMiddleware





app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://nutrition-os-frontend-acl14.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(recommendations_router)    

app.include_router(meal_log_router)      
app.include_router(profile_router)
app.include_router(nutrition_router)
app.include_router(restaurant_router)
app.include_router(meals_router)
app.include_router(my_meals_router)
app.include_router(dashboard_router)
app.include_router(ai_router)
app.include_router(analytics_router)
app.include_router(score_router)



templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


# ==========================================
# Request Model
# ==========================================

class RecommendationRequest(BaseModel):

    goal: str
    diet: str
    budget: float


# ==========================================
# Home Page
# ==========================================

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="home.html"
    )


@app.get("/login", response_class=HTMLResponse)
def login(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@app.get("/goal", response_class=HTMLResponse)
def goal(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="goal.html"
    )


@app.get("/diet", response_class=HTMLResponse)
def diet(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="diet.html"
    )


@app.get("/results", response_class=HTMLResponse)
def results(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="results.html"
    )


# ==========================================
# Restaurant Page
# ==========================================

@app.get("/restaurant/{restaurant_id}", response_class=HTMLResponse)
def restaurant_page(request: Request, restaurant_id: int):

    return templates.TemplateResponse(
        request=request,
        name="restaurant.html",
        context={
            "restaurant_id": restaurant_id
        }
    )


# ==========================================
# Get All Restaurants
# ==========================================

@app.get("/restaurants")
def get_restaurants():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM restaurants
                ORDER BY restaurant_name
            """)
        )

        restaurants = [dict(row._mapping) for row in result]

    return restaurants


# ==========================================
# Restaurant Details
# ==========================================

@app.get("/restaurants/{restaurant_id}")
def get_restaurant(restaurant_id: int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM restaurants
                WHERE restaurant_id = :restaurant_id
            """),
            {
                "restaurant_id": restaurant_id
            }
        )

        restaurant = result.fetchone()

    if restaurant:

        return dict(restaurant._mapping)

    return {"error": "Restaurant not found"}


# ==========================================
# Restaurant Menu
# ==========================================

@app.get("/restaurants/{restaurant_id}/menu")
def get_menu(restaurant_id: int):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM menu_items
                WHERE restaurant_id = :restaurant_id
                ORDER BY protein DESC
            """),
            {
                "restaurant_id": restaurant_id
            }
        )

        menu = [dict(row._mapping) for row in result]

    return menu


# ==========================================
# Recommendation API
# ==========================================

@app.post("/recommend")
def recommend(data: RecommendationRequest):

    veg_value = data.diet.lower() == "veg"

    goal = data.goal.lower()

    if goal == "muscle gain":

        order_clause = "m.protein DESC"

    elif goal == "weight loss":

        order_clause = "m.calories ASC, m.protein DESC"

    else:

        order_clause = "r.rating DESC, m.protein DESC"

    sql = f"""
        SELECT

            m.id,
            m.restaurant_id,
            m.dish_name,
            m.category,
            m.calories,
            m.protein,
            m.carbs,
            m.fat,
            m.fiber,
            m.price,
            m.is_veg,

            r.restaurant_name,
            r.address,
            r.area,
            r.rating,
            r.delivery_time

        FROM menu_items m

        JOIN restaurants r

        ON m.restaurant_id = r.restaurant_id

        WHERE

            m.price <= :budget
            AND m.is_veg = :veg
            AND m.available = true

        ORDER BY

            {order_clause}

        LIMIT 10
    """

    with engine.connect() as conn:

        result = conn.execute(
            text(sql),
            {
                "budget": data.budget,
                "veg": veg_value
            }
        )

        dishes = [dict(row._mapping) for row in result]
        # ==========================================
# Nutrition Score
# ==========================================
        for dish in dishes:

            nutrition_score = calculate_score(dish)

            goal_match = calculate_goal_match(
                data.goal,
                dish
            )

            dish["nutrition_score"] = nutrition_score

            dish["recommendation_reason"] = recommendation_reason(
                nutrition_score
            )

            dish["goal_match"] = goal_match

            dish["goal_match_label"] = goal_match_label(
                goal_match
            )
            dish["badges"] = generate_badges(dish)
            dish["ai_explanation"] = generate_explanation(
            data.goal,
            dish)
            dish["final_score"] = calculate_final_score(dish)

        dishes.sort(

            key=lambda x: x["final_score"],

            reverse=True

)
                

    return {

        "goal": data.goal,

        "diet": data.diet,

        "budget": data.budget,

        "recommended_dishes": dishes

    }