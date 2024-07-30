"""
Exceptions for the notifications app
"""
from fastapi import HTTPException, status
from pydantic import BaseModel


class NotificationNotFound(HTTPException):
    """
    Exception raised when a Notification is not found.
    """

    class NotificationNotFoundSchema(BaseModel):
        """
        Schema for the NotificationNotFound model.
        """
        detail: str = "Notification not found."

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.NotificationNotFoundSchema().detail
        )
