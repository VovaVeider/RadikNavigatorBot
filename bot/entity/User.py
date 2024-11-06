from typing import Optional

class User:
    def __init__(self, id: int, user_id: int, group_id: Optional[int], role: Optional[str]):
        self.id = id
        self.user_id = user_id
        self.group_id = group_id
        self.role = role

    def __repr__(self):
        return f"<User(id={self.id}, user_id={self.user_id}, group_id={self.group_id}, role={self.role})>"