"""
Schemas for the notifications app
"""
from pydantic import BaseModel, Field, ConfigDict


class NotificationBase(BaseModel):
    """
    Base schema for the Notification model.
    """
    user_id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1, max_length=100)
    content: str
    read: bool = False


class NotificationCreate(NotificationBase):
    """
    Schema for creating a Notification model.
    """


class Notification(NotificationBase):
    """
    Schema for the Notification model.
    """
    model_config: ConfigDict = ConfigDict(
        from_attributes=True
    )
    id: int = Field(..., gt=0)
