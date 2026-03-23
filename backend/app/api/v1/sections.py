"""Section API Router."""
from fastapi import APIRouter, status, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, require_role, get_current_user
from app.models.user import User
from app.schemas.section import SectionCreate, SectionUpdate, SectionResponse
from app.services.section_service import SectionService
from app.repositories.section_repo import SectionRepository
from app.utils.responses import success_response, error_response
from app.core.exceptions import ApplicationError

router = APIRouter(prefix="/sections", tags=["sections"])


async def get_section_service(db: AsyncSession = Depends(get_db)) -> SectionService:
    """Dependency to get section service."""
    from app.models.section import Section
    repo = SectionRepository(db, Section)
    return SectionService(repo)


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_section(
    obj_in: SectionCreate,
    service: SectionService = Depends(get_section_service),
    db: AsyncSession = Depends(get_db)
):
    """Create a new section."""
    try:
        section = await service.create_section(db, obj_in)
        return success_response(data=SectionResponse.from_orm(section).dict(), message="Section created successfully")
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/{section_id}", response_model=dict)
async def get_section(
    section_id: int,
    service: SectionService = Depends(get_section_service),
    db: AsyncSession = Depends(get_db)
):
    """Get section by ID."""
    try:
        section = await service.get_section(db, section_id)
        return success_response(data=SectionResponse.from_orm(section).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/module/{module_id}", response_model=dict)
async def get_sections_by_module(
    module_id: int,
    service: SectionService = Depends(get_section_service),
    db: AsyncSession = Depends(get_db)
):
    """Get all sections in a module."""
    try:
        sections = await service.get_sections_by_module(db, module_id)
        return success_response(data=[SectionResponse.from_orm(s).dict() for s in sections])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("", response_model=dict)
async def list_sections(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: SectionService = Depends(get_section_service),
    db: AsyncSession = Depends(get_db)
):
    """List all sections."""
    try:
        sections = await service.get_all_sections(db, skip=skip, limit=limit)
        return success_response(
            data=[SectionResponse.from_orm(s).dict() for s in sections],
            meta={"skip": skip, "limit": limit}
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.put("/{section_id}", response_model=dict)
async def update_section(
    section_id: int,
    obj_in: SectionUpdate,
    service: SectionService = Depends(get_section_service),
    db: AsyncSession = Depends(get_db)
):
    """Update section."""
    try:
        section = await service.update_section(db, section_id, obj_in)
        return success_response(data=SectionResponse.from_orm(section).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.delete("/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_section(
    section_id: int,
    current_user: User = Depends(get_current_user),
    service: SectionService = Depends(get_section_service),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete section. Requires authentication."""
    try:
        await service.delete_section(db, section_id)
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )
