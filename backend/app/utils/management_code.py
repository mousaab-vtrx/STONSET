"""
Management code generation utility for department heads and managers.
"""
import random
import string
from datetime import datetime


def generate_management_code(user_id: int, user_type: str) -> str:
    """
    Generate a unique management code for a manager.
    
    Format: {USER_TYPE_PREFIX}-{USER_ID}-{RANDOM_STRING}
    Example: DEPT-123-A7K9M2
    
    Args:
        user_id: The ID of the user
        user_type: The type of user (chef_dept, responsable_service)
    
    Returns:
        A unique management code string
    """
    # Prefix based on user type
    prefixes = {
        'chef_dept': 'DEPT',
        'responsable_service': 'SVC',
    }
    
    prefix = prefixes.get(user_type, 'MGR')
    
    # Generate random alphanumeric string (6 characters)
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # Combine parts
    code = f"{prefix}-{user_id:05d}-{random_part}"
    
    return code


def validate_management_code_format(code: str) -> bool:
    """
    Validate if a code matches the expected format.
    
    Args:
        code: The management code to validate
    
    Returns:
        True if valid format, False otherwise
    """
    parts = code.split('-')
    if len(parts) != 3:
        return False
    
    prefix, user_id, random_part = parts
    
    # Check prefix
    if prefix not in ['DEPT', 'SVC', 'MGR']:
        return False
    
    # Check user_id format (should be 5 digits)
    if not user_id.isdigit() or len(user_id) != 5:
        return False
    
    # Check random part (should be 6 alphanumeric)
    if len(random_part) != 6 or not all(c.isalnum() for c in random_part):
        return False
    
    return True
