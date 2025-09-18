import os
from datetime import datetime

class Logger:
    log_level = {
        1: "[INFO]",
        2: "[DEBUG]",
        3: "[ERROR]",
    }

    def __init__(self, log_dir="logs"):
        self.date = datetime.today().strftime('%Y%m%d%H%M')
        self.filename = f"scraper_{self.date}.log"
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    def log(self, message, log_level=1):
        level_str = self.log_level.get(log_level, "[INFO]")
        line = f"{level_str} {message}"
        print(line)
        path = os.path.join(self.log_dir, self.filename)
        with open(path, "a") as f:
            f.write(line + "\n")

