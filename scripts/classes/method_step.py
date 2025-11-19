
class step:
    def __init__(self):
        self.step_num = 0
        self.step_evaluation = False


    def next_step(self):
        self.step_num += 1
        
    def evaluate_step(self, evaluation: bool):
        self.step_evaluation = evaluation