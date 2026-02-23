import enum

class Status(enum.Enum):
    pending = "pending"
    running = "running"
    finished = "finished"
    failed = "failed"

