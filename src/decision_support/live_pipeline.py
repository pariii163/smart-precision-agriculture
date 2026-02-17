from src.digital_twin.twin_update import update_twin_state


class LiveDecisionPipeline:
    def __init__(self, twin_state, model):
        self.twin_state = twin_state
        self.model = model

    def process_new_data(self, new_data: dict):
        """
        Updates the digital twin with new data and returns a recommendation.
        """
        self.twin_state = update_twin_state(self.twin_state, new_data)
        recommendation = self.model.predict_from_twin(self.twin_state)

        return self.twin_state, recommendation
