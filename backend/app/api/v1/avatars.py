"""Avatar management endpoints."""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.utils.file_handler import FileHandler
from app.utils.responses import success_response, error_response

router = APIRouter(prefix="/api/v1/avatars", tags=["avatars"])


@router.post("/upload")
async def upload_avatar(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Upload and save user avatar.
    
    Args:
        file: Image file to upload
        session: Database session
        current_user: Authenticated user
        
    Returns:
        Success response with avatar URL
    """
    try:
        # Read file content
        content = await file.read()
        
        # Validate and save file
        avatar_url = FileHandler.save_avatar(
            file_content=content,
            original_filename=file.filename or "avatar.jpg",
            user_id=current_user.id
        )
        
        # Delete old avatar if exists
        if current_user.avatar_url:
            FileHandler.delete_avatar(current_user.avatar_url)
        
        # Update user record
        current_user.avatar_url = avatar_url
        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        
        return success_response(
            data={"avatar_url": avatar_url},
            message="Avatar uploaded successfully"
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading avatar: {str(e)}")


@router.delete("/delete")
async def delete_avatar(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Delete user avatar.
    
    Args:
        session: Database session
        current_user: Authenticated user
        
    Returns:
        Success response
    """
    try:
        if current_user.avatar_url:
            FileHandler.delete_avatar(current_user.avatar_url)
            current_user.avatar_url = None
            session.add(current_user)
            session.commit()
            session.refresh(current_user)
        
        return success_response(message="Avatar deleted successfully")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting avatar: {str(e)}")
