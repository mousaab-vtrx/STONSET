"""Department API Router."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, require_role, get_current_user
from app.models.user import User
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.services.department_service import DepartmentService
from app.repositories.department_repo import DepartmentRepository
from app.utils.responses import success_response, error_response
from app.core.exceptions import ApplicationError

router = APIRouter(prefix="/departments", tags=["departments"])


async def get_department_service(db: AsyncSession = Depends(get_db)) -> DepartmentService:
    """Dependency to get department service."""
    from app.models.department import Department
    repo = DepartmentRepository(db, Department)
    return DepartmentService(repo)


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_department(
    obj_in: DepartmentCreate,
    current_user: User = Depends(require_role("chef_dept", "responsable_service")),
    service: DepartmentService = Depends(get_department_service),
    db: AsyncSession = Depends(get_db)
):
    """Create a new department. Only chef_dept and responsable_service can create departments."""
    try:
        department = await service.create_department(db, obj_in)
        return success_response(
            data=DepartmentResponse.from_orm(department).dict(),
            message="Department created successfully"
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("/{department_id}", response_model=dict)
async def get_department(
    department_id: int,
    current_user: User = Depends(get_current_user),
    service: DepartmentService = Depends(get_department_service),
    db: AsyncSession = Depends(get_db)
):
    """Get department by ID. Requires authentication."""
    try:
        department = await service.get_department(db, department_id)
        return success_response(data=DepartmentResponse.from_orm(department).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.get("", response_model=dict)
async def list_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: DepartmentService = Depends(get_department_service),
    db: AsyncSession = Depends(get_db)
):
    """List all departments. Requires authentication."""
    try:
        departments = await service.get_all_departments(db, skip=skip, limit=limit)
        return success_response(
            data=[DepartmentResponse.from_orm(d).dict() for d in departments],
            meta={"total": len(departments), "skip": skip, "limit": limit}
        )
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.put("/{department_id}", response_model=dict)
async def update_department(
    department_id: int,
    obj_in: DepartmentUpdate,
    current_user: User = Depends(require_role("chef_dept", "responsable_service")),
    service: DepartmentService = Depends(get_department_service),
    db: AsyncSession = Depends(get_db)
):
    """Update department. Only chef_dept and responsable_service can update departments."""
    try:
        department = await service.update_department(db, department_id, obj_in)
        return success_response(data=DepartmentResponse.from_orm(department).dict())
    except ApplicationError as e:
        return error_response(
            message=e.message,
            code=getattr(e, "code", "ERROR"),
            status_code=e.status_code,
        )


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: int,
    current_user: User = Depends(require_role("chef_dept", "responsable_service")),
    service: DepartmentService = Depends(get_department_service),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete department. Only chef_dept and responsable_service can delete departments."""
    try:
        await service.delete_department(db, department_id)
    except ApplicationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
