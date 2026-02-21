from datetime import datetime, timezone
from sqlalchemy.orm import Session
from ..db.models.user import User

def update_user_streak(user: User, db: Session):
    now = datetime.now(timezone.utc)
    last_active = user.last_active_date

    if last_active is None:
        user.current_streak = 1
    else:
        delta_days = (now.date() - last_active.date()).days
        if delta_days == 0:
            return
        elif delta_days == 1:
            user.current_streak += 1
        else:
            user.current_streak = 1

    user.last_active_date = now
    db.add(user)
    db.commit()

