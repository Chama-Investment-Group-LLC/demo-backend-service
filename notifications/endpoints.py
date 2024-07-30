"""
Endpoints for the notifications app
"""
from typing import Annotated, List
from fastapi import APIRouter, Depends, Body, Query, Path
from sqlalchemy.orm import Session

from database import get_db
from auth_utils import AuthorizationException, require_user, require_admin_user, AdminUser, User

from . import crud, schemas, exceptions


router = APIRouter(
    prefix="/notification",
    tags=["notification"],
    responses={
        500: {"description": "Internal Server Error"},
    }
)


@router.post(
    "/", response_model=schemas.Notification, status_code=201,
    responses={
        401: {"model": AuthorizationException.AuthorizationErrorSchema}
    }
)
def create_notification(
    notification: Annotated[schemas.NotificationCreate, Body()],
    _: Annotated[AdminUser, Depends(require_admin_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Creates a new Notification.
    """
    return crud.create_notification(db, notification)


@router.get("/", response_model=List[schemas.Notification])
def get_all_notifications(
    user: Annotated[User, Depends(require_user)],
    db: Annotated[Session, Depends(get_db)],
    skip: Annotated[int, Query(0, ge=0)] = 0,
    limit: Annotated[int, Query(5, le=5)] = 5,
):
    """
    Returns all Notifications for a user.
    """
    return crud.get_all_notifications(db, user.id, skip, limit)


@router.patch(
    "/{notification_id}/mark_as_read", response_model=schemas.Notification,
    responses={
        401: {"model": AuthorizationException.AuthorizationErrorSchema},
        404: {"model": exceptions\
              .NotificationNotFound.NotificationNotFoundSchema}
    })
def mark_notification_as_read(
    user: Annotated[User, Depends(require_user)],
    notification_id: Annotated[int, Path(..., ge=1)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Marks a Notification as read.
    """
    return crud.mark_notification_as_read(db, user.id, notification_id)


@router.patch("/mark_all_as_read", response_model=List[schemas.Notification])
def mark_all_notifications_as_read(
    user: Annotated[User, Depends(require_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Marks all Notifications for a user as read.
    """
    return crud.mark_all_notifications_as_read(db, user.id)
