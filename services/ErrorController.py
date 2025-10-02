from services.logger import Logger

class ErrorController:
    errors = [
        500,
        404,
        405,
        406,
        407,
    ]

    def __init__(self, db):
        self.db = db
        self.logger = Logger()

    def detect(self, error):
        for error in self.errors:
            self.logger.log(f"Detected error code: {error}")
            return