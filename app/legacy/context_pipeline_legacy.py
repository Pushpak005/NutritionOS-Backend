from app.context.builder import build_context


# ==========================================
# NutritionOS Pipeline
# ==========================================

def get_context(user_id: int):

    """
    Single entry point for obtaining the
    current application context.
    """

    return build_context(user_id)