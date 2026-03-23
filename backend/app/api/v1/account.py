"""Account deletion endpoints."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.account_deletion_service import AccountDeletionService
from app.utils.responses import success_response, error_response

router = APIRouter(prefix="/account", tags=["account"])  # ✅ Fixed: removed /api/v1 prefix


class DeletionFeedbackRequest(BaseModel):
    """Request model for account deletion feedback."""
    reason: str
    additional_feedback: Optional[str] = None


class DeletionReasonsResponse(BaseModel):
    """Response model for deletion reasons."""
    reasons: list[str]


@router.get("/deletion-reasons")
async def get_deletion_reasons() -> DeletionReasonsResponse:
    """
    Get list of predefined reasons for account deletion.

    Returns:
        List of deletion reason strings
    """
    reasons = AccountDeletionService.get_deletion_reasons()  # ✅ No await
    return DeletionReasonsResponse(reasons=reasons)


@router.post("/delete", status_code=status.HTTP_200_OK)
async def delete_account(
    feedback: DeletionFeedbackRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Delete authenticated user account after collecting feedback.

    This endpoint:
    1. Validates the deletion request
    2. Saves user feedback
    3. Deletes user account and related data (cascade)
    4. Returns success message

    Args:
        feedback: Feedback data with reason and optional message
        session: Database session
        current_user: Currently authenticated user (verified ownership)

    Returns:
        Success response with message

    Raises:
        HTTPException: 400 for invalid input, 401 for auth, 500 for server error
    """
    # ✅ Verify user is authenticated and active
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to delete account"
        )
    
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is already inactive or has been deleted"
        )
    
    try:
        # Validate reason is in predefined list
        valid_reasons = AccountDeletionService.get_deletion_reasons()
        if feedback.reason not in valid_reasons:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid reason. Must be one of: {', '.join(valid_reasons)}"
            )

        # ✅ Validate additional feedback if "Other" is selected
        if feedback.reason == "Other":
            if not feedback.additional_feedback or not feedback.additional_feedback.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Please provide additional feedback when selecting 'Other'"
                )
            if len(feedback.additional_feedback) > 1000:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Additional feedback must be 1000 characters or less"
                )

        # ✅ Save deletion feedback before account deletion
        await AccountDeletionService.save_deletion_feedback(
            session=session,
            user_id=current_user.id,
            reason=feedback.reason,
            additional_feedback=feedback.additional_feedback
        )

        # ✅ Delete user account (cascade handles related records)
        success = await AccountDeletionService.delete_user_account(
            session=session,
            user_id=current_user.id
        )

        if not success:
            await session.rollback()  # ✅ Rollback on failure
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete account. Please try again."
            )

        # ✅ Commit transaction after successful deletion
        await session.commit()

        return success_response(
            message="Your account has been successfully deleted. Thank you for your feedback!"
        )

    except HTTPException:
        await session.rollback()  # ✅ Rollback on any HTTP error
        raise
    except Exception as e:
        await session.rollback()  # ✅ Rollback on unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting account"
        )


@router.get("/auth/me", response_model=dict)
def get_authenticated_user(current_user: User = Depends(get_current_user)):
    """
    Endpoint to retrieve the current authenticated user's details.
    """
    return success_response(
        data=UserResponse.from_orm(current_user).dict(),
        message="Current user retrieved successfully"
    )
