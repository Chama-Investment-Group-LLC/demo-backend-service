"""
Notifications Models.
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import validates

from database import Base


class Notification(Base):
    """
    Notification Model.
    """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(String, nullable=False)
    read = Column(Boolean, default=False, nullable=False)

    @validates("user_id")
    def validate_user_id(self, _, user_id):
        """
        Validates the user_id attribute.
        """
        if user_id < 1:
            raise ValueError("user_id must be greater than 0.")
        return user_id

    @validates("title")
    def validate_title(self, _, title):
        """
        Validates the title attribute.
        """
        if len(title) < 1:
            raise ValueError("title must not be empty.")
        return title
