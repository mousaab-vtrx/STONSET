"""Module (Course) API Router."""
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user, require_role
from app.models.user import User
from app.schemas.module import ModuleCreate, ModuleUpdate, ModuleResponse
from app.services.module_service import ModuleService
from app.repositories.module_repo import ModuleRepository
from app.utils.responses import success_response, error_response
from app.core.exceptions import ApplicationError

router = APIRouter(prefix="/modules", tags=["modules"])


async def get_module_service(db: AsyncSession = Depends(get_db)) -> ModuleService:
    """Dependency to get module service."""
    from app.models.module import Module
    repo = ModuleRepository(db, Module)
    return ModuleService(repo)


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_module(
    obj_in: ModuleCreate,
    current_user: User = Depends(require_role("responsable_service", "chef_dept")),
    service: ModuleService = Depends(get_module_service),
    db: AsyncSession = Depends(get_db)
):
    """Create a new course/module. Only service managers and department heads can create modules."""
    try:
        module = await service.create_module(db, obj_in)
        return success_response(data=ModuleResponse.from_orm(module).dict(), message="Module created successfully")
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/{module_id}", response_model=dict)
async def get_module(
    module_id: int,
    current_user: User = Depends(get_current_user),
    service: ModuleService = Depends(get_module_service),
    db: AsyncSession = Depends(get_db)
):
    """Get module by ID. Requires authentication."""
    try:
        module = await service.get_module(db, module_id)
        return success_response(data=ModuleResponse.from_orm(module).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/code/{code}", response_model=dict)
async def get_module_by_code(
    code: str,
    current_user: User = Depends(get_current_user),
    service: ModuleService = Depends(get_module_service),
    db: AsyncSession = Depends(get_db)
):
    """Get module by code. Requires authentication."""
    try:
        module = await service.get_module_by_code(db, code)
        return success_response(data=ModuleResponse.from_orm(module).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/filiere/{filiere_id}", response_model=dict)
async def get_modules_by_filiere(
    filiere_id: int,
    current_user: User = Depends(get_current_user),
    service: ModuleService = Depends(get_module_service),
    db: AsyncSession = Depends(get_db)
):
    """Get all modules in a program. Requires authentication."""
    try:
        modules = await service.get_modules_by_filiere(db, filiere_id)
        return success_response(data=[ModuleResponse.from_orm(m).dict() for m in modules])
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("", response_model=dict)
async def list_modules(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: ModuleService = Depends(get_module_service),
    db: AsyncSession = Depends(get_db)
):
    """List all modules. Requires authentication."""
    try:
        modules = await service.get_all_modules(db, skip=skip, limit=limit)
        return success_response(
            data=[ModuleResponse.from_orm(m).dict() for m in modules],
            meta={"skip": skip, "limit": limit}
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.put("/{module_id}", response_model=dict)
async def update_module(
    module_id: int,
    obj_in: ModuleUpdate,
    current_user: User = Depends(require_role("responsable_service", "chef_dept")),
    service: ModuleService = Depends(get_module_service),
    db: AsyncSession = Depends(get_db)
):
    """Update module. Only service managers and department heads can update modules."""
    try:
        module = await service.update_module(db, module_id, obj_in)
        return success_response(data=ModuleResponse.from_orm(module).dict())
    except ApplicationError as e:
        return error_response(message=e.message, status_code=e.status_code)


@router.delete("/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_module(
    module_id: int,
    current_user: User = Depends(require_role("responsable_service", "chef_dept")),
    service: ModuleService = Depends(get_module_service),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete module. Only service managers and department heads can delete modules."""
    try:
        await service.delete_module(db, module_id)
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )
