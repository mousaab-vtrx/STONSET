"""
Management API - Endpoints for managers to manage subordinates.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.db.session import async_session
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.services.management_service import ManagementService
from app.schemas.user import UserResponse
from app.utils.responses import success_response, error_response

router = APIRouter(prefix="/api/v1/management", tags=["management"])


async def get_management_service(db: AsyncSession = Depends(get_db)) -> ManagementService:
    """Get management service."""
    user_repo = UserRepository(db)
    return ManagementService(user_repo)


@router.get("/subordinates")
async def list_subordinates(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Get all subordinates of the current manager.
    
    Requires: User must be chef_dept or responsable_service
    """
    if current_user.user_type not in ['chef_dept', 'responsable_service']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can view subordinates"
        )
    
    management_service = ManagementService(UserRepository(db))
    subordinates = await management_service.get_subordinates(db, current_user.id)
    
    subordinates_data = [
        UserResponse(
            id=s.id,
            email=s.email,
            nom_user=s.nom_user,
            prenom_user=s.prenom_user,
            user_type=s.user_type,
            is_active=s.is_active,
            management_code=s.management_code,
        )
        for s in subordinates
    ]
    
    return success_response(subordinates_data)


@router.get("/code")
async def get_management_code(
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Get the management code for the current user.
    
    Requires: User must be chef_dept or responsable_service
    """
    if current_user.user_type not in ['chef_dept', 'responsable_service']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can have management codes"
        )
    
    if not current_user.management_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Management code not generated yet"
        )
    
    return success_response({
        "management_code": current_user.management_code,
        "user_id": current_user.id,
        "user_type": current_user.user_type,
    })


@router.post("/code/generate")
async def generate_management_code(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Generate a new management code for the current user.
    
    Requires: User must be chef_dept or responsable_service
    """
    if current_user.user_type not in ['chef_dept', 'responsable_service']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can generate codes"
        )
    
    management_service = ManagementService(UserRepository(db))
    
    try:
        code = await management_service.generate_management_code(db, current_user.id)
        await db.commit()
        
        return success_response({
            "management_code": code,
            "message": "Management code generated successfully"
        })
    except ValueError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/subordinates/{subordinate_id}")
async def remove_subordinate(
    subordinate_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Remove a subordinate from the current manager.
    
    Requires: User must be chef_dept or responsable_service
    """
    if current_user.user_type not in ['chef_dept', 'responsable_service']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can remove subordinates"
        )
    
    management_service = ManagementService(UserRepository(db))
    
    success = await management_service.remove_subordinate(db, current_user.id, subordinate_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subordinate not found or not managed by you"
        )
    
    await db.commit()
    
    return success_response({
        "message": "Subordinate removed successfully"
    })


@router.get("/subordinates/recursive")
async def list_all_subordinates_recursive(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Get all subordinates recursively (subordinates of subordinates).
    
    Requires: User must be chef_dept or responsable_service
    """
    if current_user.user_type not in ['chef_dept', 'responsable_service']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can view subordinates"
        )
    
    management_service = ManagementService(UserRepository(db))
    subordinates = await management_service.list_all_subordinates_recursive(db, current_user.id)
    
    subordinates_data = [
        UserResponse(
            id=s.id,
            email=s.email,
            nom_user=s.nom_user,
            prenom_user=s.prenom_user,
            user_type=s.user_type,
            is_active=s.is_active,
            management_code=s.management_code,
        )
        for s in subordinates
    ]
    
    return success_response(subordinates_data)
