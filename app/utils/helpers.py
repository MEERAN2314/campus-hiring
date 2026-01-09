from bson import ObjectId
from typing import Any, Dict
import re


def object_id_to_str(obj: Any) -> Any:
    """Convert ObjectId to string in dict/list"""
    if isinstance(obj, dict):
        return {k: object_id_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [object_id_to_str(item) for item in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    return obj


def generate_id() -> str:
    """Generate a new ObjectId as string"""
    return str(ObjectId())


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove any path components
    filename = filename.split('/')[-1].split('\\')[-1]
    # Remove special characters except dots and dashes
    filename = re.sub(r'[^\w\s.-]', '', filename)
    return filename


def calculate_percentage(score: float, max_score: int) -> float:
    """Calculate percentage score"""
    if max_score == 0:
        return 0.0
    return round((score / max_score) * 100, 2)


def format_duration(seconds: int) -> str:
    """Format duration in seconds to human readable format"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"
