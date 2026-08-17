from app.core.contracts.provider_contract import ProviderContract


class HealthConnectProvider(ProviderContract):

    """
    Health Connect Provider

    Prototype:
        Safe zero/default values.

    Future:
        Android Health Connect
        Samsung Health
        Wearables
    """

    # ==========================================
    # User
    # ==========================================

    def get_user(self, user_id: int):

        return {
            "user_id": user_id,
            "goal": None
        }

    # ==========================================
    # Nutrition
    # ==========================================

    def get_nutrition(self, user_id: int):

        return {
            "daily_calories": 0,
            "daily_protein": 0,
            "consumed_calories": 0,
            "consumed_protein": 0
        }

    # ==========================================
    # Activity
    # ==========================================

    def get_activity(self, user_id: int):

        """
        Normalized activity contract.

        Future Android Health Connect data
        will populate these fields.
        """

        return {

            "steps": 0,

            "calories_burned": 0,

            "workout_today": False,

            "active_minutes": 0,

            "distance_km": 0,

            "activity_source": "none"

        }

    # ==========================================
    # Device
    # ==========================================

    def get_device(self, user_id: int):

        return {

            "health_connected": False,

            "provider": "health_connect"

        }