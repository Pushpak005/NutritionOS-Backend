from sqlalchemy import text

from app.database import engine


def recommend_meals(user_id: int):

    with engine.connect() as conn:

        user = conn.execute(
            text("""
                SELECT
                    goal,
                    diet_preferences,
                    daily_budget,
                    daily_calories,
                    daily_protein
                FROM users
                WHERE id=:id
            """),
            {"id": user_id}
        ).fetchone()

        consumed = conn.execute(
            text("""
                SELECT

                    COALESCE(SUM(mi.calories*m.quantity),0) calories,

                    COALESCE(SUM(mi.protein*m.quantity),0) protein

                FROM meals m

                JOIN menu_items mi

                ON m.menu_item_id=mi.id

                WHERE m.user_id=:id
            """),
            {"id": user_id}
        ).fetchone()

        remaining_calories = (
            user.daily_calories -
            consumed.calories
        )

        remaining_protein = (
            user.daily_protein -
            consumed.protein
        )

        menu = conn.execute(
            text("""
                SELECT

                    id,

                    dish_name,

                    calories,

                    protein,

                    price,

                    is_veg

                FROM menu_items

                WHERE available=true
            """)
        ).fetchall()

    recommendations=[]

    for meal in menu:

        score=0

        if meal.calories <= remaining_calories:
            score+=40

        if meal.protein <= remaining_protein:
            score+=30

        if meal.price <= user.daily_budget:
            score+=20

        if (
            user.diet_preferences=="Veg"
            and meal.is_veg
        ):
            score+=10

        recommendations.append({

            "score":score,

            **dict(meal._mapping)

        })

    recommendations.sort(

        key=lambda x:x["score"],

        reverse=True

    )

    return{

        "remaining_calories":remaining_calories,

        "remaining_protein":remaining_protein,

        "recommendations":recommendations[:3]

    }