from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.database import engine
from app.utils.auth_dependency import get_current_user
from app.schemas.user import UserProfileUpdate
from app.services.nutrition_engine import calculate_nutrition
from app.services.recommendation_engine import calculate_nutrition_score


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ==========================================
# Get Current User Profile
# ==========================================

@router.get("/me")
def get_my_profile(current_user=Depends(get_current_user)):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    id,
                    name,
                    email,
                    age,
                    gender,
                    height_cm,
                    weight_kg,
                    goal,
                    diet_preferences,
                    daily_budget,
                    activity_level,
                    daily_calories,
                    daily_protein,
                    daily_carbs,
                    daily_fat,
                    daily_fiber,
                    bmi,
                    target_weight,
                    allergies,
                    health_conditions
                FROM users
                WHERE id = :id
            """),
            {
                "id": current_user["user_id"]
            }
        ).fetchone()

    if result is None:
        return {
            "success": False,
            "message": "User not found."
        }

    return dict(result._mapping)


# ==========================================
# Update Current User Profile
# ==========================================

@router.put("/me")
def update_my_profile(
    profile: UserProfileUpdate,
    current_user=Depends(get_current_user)
):

    update_data = profile.model_dump(exclude_none=True)

    if not update_data:
        return {
            "success": False,
            "message": "No fields provided for update."
        }

    # ==========================================
    # Load Existing Profile
    # ==========================================

    with engine.connect() as conn:

        current_user_data = conn.execute(
            text("""
                SELECT
                    age,
                    gender,
                    height_cm,
                    weight_kg,
                    goal,
                    activity_level
                FROM users
                WHERE id = :id
            """),
            {
                "id": current_user["user_id"]
            }
        ).fetchone()

    current_user_data = dict(current_user_data._mapping)

    # Merge existing values with updated values

    nutrition_profile = {
        "age": update_data.get("age", current_user_data["age"]),
        "gender": update_data.get("gender", current_user_data["gender"]),
        "height_cm": update_data.get("height_cm", current_user_data["height_cm"]),
        "weight_kg": update_data.get("weight_kg", current_user_data["weight_kg"]),
        "goal": update_data.get("goal", current_user_data["goal"]),
        "activity_level": update_data.get(
            "activity_level",
            current_user_data["activity_level"]
        )
    }

    # ==========================================
    # Calculate Nutrition
    # ==========================================

    nutrition = calculate_nutrition(nutrition_profile)

    update_data["bmi"] = nutrition["bmi"]
    update_data["daily_calories"] = nutrition["daily_calories"]
    update_data["daily_protein"] = nutrition["daily_protein"]
    update_data["daily_carbs"] = nutrition["daily_carbs"]
    update_data["daily_fat"] = nutrition["daily_fat"]
    update_data["daily_fiber"] = nutrition["daily_fiber"]

    # ==========================================
    # Dynamic UPDATE Query
    # ==========================================

    set_clause = ", ".join(
        [f"{column} = :{column}" for column in update_data.keys()]
    )

    update_data["id"] = current_user["user_id"]

    query = text(f"""
        UPDATE users
        SET {set_clause}
        WHERE id = :id
    """)

    with engine.begin() as conn:

        conn.execute(query, update_data)

        updated_user = conn.execute(
            text("""
                SELECT
                    id,
                    name,
                    email,
                    age,
                    gender,
                    height_cm,
                    weight_kg,
                    goal,
                    diet_preferences,
                    daily_budget,
                    activity_level,
                    daily_calories,
                    daily_protein,
                    daily_carbs,
                    daily_fat,
                    daily_fiber,
                    bmi,
                    target_weight,
                    allergies,
                    health_conditions
                FROM users
                WHERE id = :id
            """),
            {
                "id": current_user["user_id"]
            }
        ).fetchone()

    return {
        "success": True,
        "message": "Profile updated successfully.",
        "user": dict(updated_user._mapping)
    }
@router.get("/recommendations/test")
def test_recommendations():

    user = {
        "daily_calories": 2163,
        "daily_protein": 135,
        "goal": "Weight Loss",
        "diet_preferences": "Veg",
        "daily_budget": 400
    }

    dishes = [
        {
            "name": "Paneer Protein Bowl",
            "calories": 620,
            "protein": 35,
            "fat": 14,
            "price": 320,
            "category": "Veg"
        },
        {
            "name": "Veg Burger",
            "calories": 850,
            "protein": 15,
            "fat": 28,
            "price": 220,
            "category": "Veg"
        },
        {
            "name": "Greek Salad",
            "calories": 380,
            "protein": 22,
            "fat": 10,
            "price": 280,
            "category": "Veg"
        },
        {
            "name": "Chicken Biryani",
            "calories": 900,
            "protein": 28,
            "fat": 30,
            "price": 350,
            "category": "Non Veg"
        }
    ]

    recommendations = []

    for dish in dishes:
        score = calculate_nutrition_score(user, dish)

        recommendations.append({
            **dish,
            "score": score
        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations