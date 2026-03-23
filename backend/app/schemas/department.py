"""Department Schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class DepartmentBase(BaseModel):
    """Base schema for department."""
    nom_department: str = Field(..., description="Department name")
    description: Optional[str] = None
    chef_department_id: Optional[int] = None


class DepartmentCreate(DepartmentBase):
    """Schema for creating department."""
    pass


class DepartmentUpdate(BaseModel):
    """Schema for updating department."""
    nom_department: Optional[str] = None
    description: Optional[str] = None
    chef_department_id: Optional[int] = None


class DepartmentResponse(DepartmentBase):
    """Schema for department response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
