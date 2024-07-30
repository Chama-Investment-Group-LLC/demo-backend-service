"""
CRUD operations for the Notification model.
"""
from typing import List
from sqlalchemy.orm import Session

from . import models, schemas, exceptions


def create_notification(
        db: Session, notification: schemas.NotificationCreate
    ) -> models.Notification:
    """
    Creates a new Notification.
    """
    db_notification = models.Notification(**notification.model_dump())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def get_all_notifications(
        db: Session, user_id: int, skip: int = 0, limit: int = 5
    ) -> List[models.Notification]:
    """
    Returns all Notifications for a user.
    """
    return db.query(models.Notification).filter(
        models.Notification.user_id == user_id
    ).order_by(models.Notification.id.desc()).offset(
        skip).limit(limit).all()


def get_notification_by_id(
        db: Session, user_id: int, notification_id: int) -> models.Notification:
    """
    Returns a Notification with selected id.
    """
    notification_db = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == user_id
    ).one_or_none()
    if notification_db is None:
        raise exceptions.NotificationNotFound()
    return notification_db


def mark_notification_as_read(
        db: Session, user_id: int, notification_id: int) -> models.Notification:
    """
    Marks a Notification as read.
    """
    notification_db = get_notification_by_id(db, user_id, notification_id)
    notification_db.read = True
    db.commit()
    db.refresh(notification_db)
    return notification_db


def mark_all_notifications_as_read(
        db: Session, user_id: int) -> List[models.Notification]:
    """
    Marks all Notifications for a user as read.
    """
    notifications_db = get_all_notifications(db, user_id)
    for notification in notifications_db:
        notification.read = True
    db.commit()
    return notifications_db


def delete_exceeded_notifications(
        db: Session, user_id: int) -> int:
    """
    Deletes exceeded Notifications for a user.
    """
    notifications_db = get_all_notifications(db, user_id, 5)
    for notification in notifications_db:
        db.delete(notification)
    db.commit()
    return len(notifications_db)
