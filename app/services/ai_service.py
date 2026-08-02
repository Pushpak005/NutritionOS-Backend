from sqlalchemy import text

from app.database import engine


def recommend_meals(user_id: int):

    with engine.connect() as conn:

        user = conn.execute(

            text("""

                SELECT

                    name,

                    goal,

                    diet_preferences,

                    daily_budget,

                    daily_calories,

                    daily_protein

                FROM users

                WHERE id=:id

            """),

            {

                "id": user_id

            }

        ).fetchone()

        consumed = conn.execute(

            text("""

                SELECT

                    COALESCE(SUM(mi.calories * CAST(m.quantity AS NUMERIC)),0) calories,

                    COALESCE(SUM(CAST(mi.protein AS NUMERIC) * CAST(m.quantity AS NUMERIC)),0) protein

                FROM meals m

                JOIN menu_items mi

                ON m.menu_item_id = mi.id

                WHERE m.user_id=:id

            """),

            {

                "id": user_id

            }

        ).fetchone()

        remaining_calories = max(

            0,

            user.daily_calories - consumed.calories

        )

        remaining_protein = max(

            0,

            user.daily_protein - consumed.protein

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

                WHERE available = true

            """)

        ).fetchall()

    recommendations = []

    for meal in menu:

        score = 0

        if meal.calories <= remaining_calories:
            score += 40

        if meal.protein <= remaining_protein:
            score += 30

        if meal.price <= user.daily_budget:
            score += 20

        if (

            user.diet_preferences == "Veg"

            and meal.is_veg

        ):

            score += 10

        recommendations.append({

            "score": score,

            **dict(meal._mapping)

        })

    recommendations.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    top_meals = recommendations[:3]

    if top_meals:

        best = top_meals[0]

        ai_message = (

            f"Hi {user.name} 👋\n\n"

            f"You still have {remaining_calories:.0f} calories "

            f"and {remaining_protein:.0f}g protein remaining today.\n\n"

            f"My top recommendation is "

            f"'{best['dish_name']}'.\n\n"

            f"It contains {best['protein']}g protein, "

            f"{best['calories']} kcal "

            f"and costs ₹{best['price']}.\n\n"

            f"This meal supports your "

            f"{user.goal} goal "

            f"while staying within your daily nutrition target."

        )

    else:

        ai_message = (

            "No suitable meal recommendations are available right now."

        )

    return {

        "remaining_calories": remaining_calories,

        "remaining_protein": remaining_protein,

        "recommendations": top_meals,

        "ai_message": ai_message

    }