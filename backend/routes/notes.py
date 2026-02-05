from fastapi import Depends, status, HTTPException, APIRouter

from ..db.models.user import User
from ..dependecies import get_current_user


router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def add_note(current_user: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Adding notes not implemented yet"
    )

@router.get("/", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def get_notes(current_user: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Retrieving notes not implemented yet"
    )

@router.get("/{note_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def get_note(note_id: int, current_user: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Retrieving notes by id not implemented yet"
    )

@router.patch("/{note_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def update_note(note_id: int, current_user: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Updating notes not implemented yet"
    )

@router.delete("/{note_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def delete_note(note_id: int, current_user: User = Depends(get_current_user)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Removing notes not implemented yet"
    )

