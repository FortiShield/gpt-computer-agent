from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseSettings, Field, PostgresDsn, validator, AnyHttpUrl, EmailStr
from typing import Optional, Dict, Any, List, Union, Literal
from pathlib import Path
import os
import secrets
import platform
import loguru
from loguru import logger

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Aideck"
    VERSION: str = "0.29.0"
    DEBUG: bool = False
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    # API Settings
    API_PREFIX: str = "/api"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:8000"]
    
    # Authentication
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    JWT_ALGORITHM: str = "HS256"
    JWT_ISSUER: str = "aideck"
    
    # First user (admin) - for initial setup
    FIRST_SUPERUSER: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "changeme"
    
    # Security
    SECURITY_BCRYPT_ROUNDS: int = 12
    
    # Database
    DATABASE_URL: Optional[PostgresDsn] = "sqlite:///./gpt_agent.db"
    
    # LLM Settings
    LLM_PROVIDER: str = "openai"
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Storage
    UPLOAD_DIR: Path = Path("./uploads")
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # Rate limiting
    RATE_LIMIT: str = "100/minute"
    
    # Audio Settings
    ENABLE_STT: bool = True
    ENABLE_TTS: bool = True
    DEFAULT_VOICE: str = "alloy"
    
    # Platform specific settings
    IS_WINDOWS: bool = platform.system() == "Windows"
    IS_MACOS: bool = platform.system() == "Darwin"
    IS_LINUX: bool = platform.system() == "Linux"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True
    
    @validator("DATABASE_URL")
    def validate_database_url(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return "sqlite:///./gpt_agent.db"
        return v

# Initialize settings
try:
    settings = Settings()
except Exception as e:
    logger.error(f"Error loading settings: {e}")
    raise

def configure_logging():
    """Configure logging with loguru"""
    import sys
    from loguru import logger
    
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
        colorize=True
    )
    
    # Add file logging in production
    if not settings.DEBUG:
        log_path = Path("logs")
        log_path.mkdir(exist_ok=True)
        logger.add(
            log_path / "gpt_agent.log",
            rotation="100 MB",
            retention="30 days",
            level=settings.LOG_LEVEL,
            format=settings.LOG_FORMAT,
            enqueue=True  # For async logging
        )

# Configure logging when the module is imported
configure_logging()
