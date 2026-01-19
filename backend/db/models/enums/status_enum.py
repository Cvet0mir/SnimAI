import enum

class Status(enum.Enum):
    pending = "pending"
    running = "running"
    done = "done"
    failed = "failed"

