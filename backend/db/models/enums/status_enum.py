import enum

class Status(enum.Enum):
    pending = "PENDING"
    running = "RUNNING"
    finished = "FINISHED"
    failed = "FAILED"

