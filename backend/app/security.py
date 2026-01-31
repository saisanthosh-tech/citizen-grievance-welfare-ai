"""
Security utilities for the Grievance System
Implements rate limiting, validation, and security best practices
"""

import re
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """Rate limiter for API endpoints to prevent abuse"""
    
    def __init__(self, enabled: bool = True, requests_per_window: int = 100, window_seconds: int = 60):
        self.enabled = enabled
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = {}
    
    def allow_request(self, client_id: str = "anonymous") -> bool:
        """Check if request is allowed based on rate limit"""
        if not self.enabled:
            return True
        
        now = time.time()
        
        # Initialize client if not exists
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Remove old requests outside the window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_seconds
        ]
        
        # Check if limit exceeded
        if len(self.requests[client_id]) >= self.requests_per_window:
            logger.warning(f"Rate limit exceeded for client: {client_id}")
            return False
        
        # Add new request
        self.requests[client_id].append(now)
        return True


class InputValidator:
    """Validate and sanitize user inputs"""
    
    # Regular expressions for validation
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    PHONE_REGEX = re.compile(r'^[0-9]{10}$')
    ALPHANUMERIC_REGEX = re.compile(r'^[a-zA-Z0-9\s\-_.(),]*$')
    
    @staticmethod
    def validate_text(text: str, min_length: int = 1, max_length: int = 5000) -> tuple[bool, str]:
        """Validate text input"""
        if not isinstance(text, str):
            return False, "Input must be text"
        
        text = text.strip()
        
        if len(text) < min_length:
            return False, f"Input must be at least {min_length} characters"
        
        if len(text) > max_length:
            return False, f"Input must not exceed {max_length} characters"
        
        return True, text
    
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Remove potentially dangerous characters from text"""
        # Remove control characters
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @staticmethod
    def validate_email(email: str) -> tuple[bool, str]:
        """Validate email address"""
        if not isinstance(email, str):
            return False, "Email must be text"
        
        email = email.strip().lower()
        
        if len(email) > 254:
            return False, "Email too long"
        
        if InputValidator.EMAIL_REGEX.match(email):
            return True, email
        
        return False, "Invalid email format"
    
    @staticmethod
    def validate_phone(phone: str) -> tuple[bool, str]:
        """Validate phone number"""
        if not isinstance(phone, str):
            return False, "Phone must be text"
        
        phone = phone.replace("-", "").replace(" ", "").replace("+91", "")
        
        if InputValidator.PHONE_REGEX.match(phone):
            return True, phone
        
        return False, "Invalid phone number (must be 10 digits)"
    
    @staticmethod
    def validate_category(category: str) -> tuple[bool, str]:
        """Validate category is one of allowed values"""
        valid_categories = [
            "Healthcare",
            "Education",
            "Water Supply",
            "Roads & Transport",
            "Electricity",
            "Sanitation"
        ]
        
        if category in valid_categories:
            return True, category
        
        return False, f"Invalid category. Must be one of: {', '.join(valid_categories)}"
    
    @staticmethod
    def validate_status(status: str) -> tuple[bool, str]:
        """Validate status is one of allowed values"""
        valid_statuses = ["Pending", "In Progress", "Resolved", "Rejected"]
        
        if status in valid_statuses:
            return True, status
        
        return False, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"


class DataSanitizer:
    """Sanitize data to prevent injection attacks"""
    
    @staticmethod
    def sanitize_sql_string(value: str) -> str:
        """Escape SQL special characters"""
        if not isinstance(value, str):
            return str(value)
        
        # Escape single quotes
        return value.replace("'", "''")
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """Remove HTML tags and potentially dangerous characters"""
        if not isinstance(text, str):
            return str(text)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # HTML entity encoding for special characters
        replacements = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;'
        }
        for char, entity in replacements.items():
            text = text.replace(char, entity)
        return text
    
    @staticmethod
    def sanitize_dict(data: dict) -> dict:
        """Sanitize all string values in a dictionary"""
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized[key] = DataSanitizer.sanitize_html(value)
            elif isinstance(value, dict):
                sanitized[key] = DataSanitizer.sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    DataSanitizer.sanitize_html(item) if isinstance(item, str) else item
                    for item in value
                ]
            else:
                sanitized[key] = value
        return sanitized


class AuditLogger:
    """Log security-relevant events"""
    
    def __init__(self):
        self.logger = logging.getLogger("audit")
        self.logger.setLevel(logging.INFO)
        
        # Create audit log file handler
        handler = logging.FileHandler("logs/audit.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_grievance_submission(self, grievance_id: str, category: str, user_location: str = "Unknown"):
        """Log grievance submission"""
        self.logger.info(
            f"Grievance submitted: ID={grievance_id}, Category={category}, Location={user_location}"
        )
    
    def log_grievance_update(self, grievance_id: str, status: str, admin_id: str = "Unknown"):
        """Log grievance status update"""
        self.logger.info(
            f"Grievance updated: ID={grievance_id}, Status={status}, Admin={admin_id}"
        )
    
    def log_access_attempt(self, endpoint: str, method: str, ip_address: str, success: bool):
        """Log API access attempt"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(
            f"API Access: {method} {endpoint} from {ip_address} - {status}"
        )
    
    def log_suspicious_activity(self, activity: str, details: str):
        """Log suspicious activity"""
        self.logger.warning(
            f"Suspicious Activity Detected: {activity} - {details}"
        )


class PasswordValidator:
    """Validate password strength"""
    
    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """
        Validate password strength
        Requirements:
        - At least 12 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        """
        if len(password) < 12:
            return False, "Password must be at least 12 characters"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            return False, "Password must contain at least one special character"
        
        return True, "Password is strong"


# Initialize audit logger
audit_logger = AuditLogger()
