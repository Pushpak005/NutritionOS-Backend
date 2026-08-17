from app.core.context.context_factory import ContextFactory


class CoreService:

    def __init__(self):

        self.context_factory = ContextFactory()

    def get_context(self, user_id: int):

        return self.context_factory.build(user_id)