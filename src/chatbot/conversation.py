class ConversationState:
    def __init__(self):
        self.condition = None
        self.data = {}
        self.current_field = None

    def set_condition(self, condition: str):
        self.condition = condition

    def set_current_field(self, field: str | None):
        self.current_field = field

    def add_data(self, field: str, value):
        if value is not None:
            self.data[field] = value
