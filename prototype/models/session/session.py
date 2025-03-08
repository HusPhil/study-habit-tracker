class Session:
    def __init__(self, id: int, duration: int, subject_id: int, goals):
        self.id = id
        self.subject_id = subject_id
        self.duration = duration
        self.goals = goals
        self.accumulated_exp = 0


    def start(self):
        """Start the session"""
        # Logic to start the session
        pass

    def stop(self):
        """End the session"""
        # Logic to end the session
        pass

    