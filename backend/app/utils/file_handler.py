"""File handling utilities for avatar uploads and storage."""
import os
import uuid
from pathlib import Path
from datetime import datetime


class FileHandler:
    """Handle file uploads, particularly for user avatars."""
    
    # Base upload directory
    UPLOAD_DIR = Path(__file__).parent.parent.parent / "uploads"
    AVATARS_DIR = UPLOAD_DIR / "avatars"
    
    # Create directories if they don't exist
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    AVATARS_DIR.mkdir(parents=True, exist_ok=True)
    
    # File size limits (in bytes)
    MAX_AVATAR_SIZE = 2 * 1024 * 1024  # 2MB
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    
    @staticmethod
    def save_avatar(file_content: bytes, original_filename: str, user_id: int) -> str:
        """
        Save an avatar file and return the relative path.
        
        Args:
            file_content: Binary content of the file
            original_filename: Original filename
            user_id: User ID for organizing files
            
        Returns:
            Relative path to the saved file
            
        Raises:
            ValueError: If file is invalid or too large
        """
        # Check file size
        if len(file_content) > FileHandler.MAX_AVATAR_SIZE:
            raise ValueError(f"File size exceeds {FileHandler.MAX_AVATAR_SIZE / (1024*1024)}MB limit")
        
        # Check file extension
        file_ext = Path(original_filename).suffix.lower()
        if file_ext not in FileHandler.ALLOWED_EXTENSIONS:
            raise ValueError(f"File type {file_ext} not allowed. Allowed: {FileHandler.ALLOWED_EXTENSIONS}")
        
        # Create user-specific directory
        user_avatar_dir = FileHandler.AVATARS_DIR / f"user_{user_id}"
        user_avatar_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = user_avatar_dir / unique_filename
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        # Return relative path from backend root
        relative_path = f"/uploads/avatars/user_{user_id}/{unique_filename}"
        return relative_path
    
    @staticmethod
    def delete_avatar(avatar_url: str) -> bool:
        """
        Delete an avatar file.
        
        Args:
            avatar_url: URL path of the avatar
            
        Returns:
            True if deleted, False if file not found
        """
        if not avatar_url:
            return False
        
        # Convert URL to file path
        # avatar_url is like "/uploads/avatars/user_123/uuid.jpg"
        file_path = FileHandler.UPLOAD_DIR / avatar_url.lstrip('/')
        
        try:
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting avatar: {e}")
            return False
    
    @staticmethod
    def get_upload_dir() -> Path:
        """Get the upload directory path."""
        return FileHandler.UPLOAD_DIR
