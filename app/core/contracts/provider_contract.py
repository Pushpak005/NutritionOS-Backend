from abc import ABC, abstractmethod


class ProviderContract(ABC):

    """
    Every data source must implement this contract.

    Today:
        - Manual Provider

    Tomorrow:
        - Health Connect
        - Samsung Health
        - Garmin
        - Fitbit
        - Apple Health
    """

    @abstractmethod
    def get_user(self, user_id: int):
        pass

    @abstractmethod
    def get_nutrition(self, user_id: int):
        pass

    @abstractmethod
    def get_activity(self, user_id: int):
        pass

    @abstractmethod
    def get_device(self, user_id: int):
        pass