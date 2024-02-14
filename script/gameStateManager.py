class GameStateManager:
    def __init__(self, currentState) -> None:
        self.currentState = currentState
        self.infos = None

    def get_state(self):
        return self.currentState

    def set_state(self, state) -> None:
        self.currentState = state
    
    def pass_info(self, **info):
        self.infos = info
