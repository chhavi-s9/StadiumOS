"""
=========================================================
config.py

Central configuration for StadiumOS AI.

Responsibilities
----------------
- Load environment variables
- Store application settings
- Store simulation constants
- Store prediction settings
- Configure logging

Every backend module imports configuration from here.

=========================================================
"""

from functools import lru_cache
import logging

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
    )

    # =====================================================
    # SERVER
    # =====================================================
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # =====================================================
    # OPENROUTER
    # =====================================================
    OPENROUTER_API_KEY: str = ""

    DEFAULT_MODEL: str = "google/gemini-2.5-flash"
    FALLBACK_MODEL: str = "deepseek/deepseek-chat-v3"

    MODEL_TEMPERATURE: float = 0.2
    MAX_OUTPUT_TOKENS: int = 1024

    # =====================================================
    # STADIUM CONFIGURATION
    # =====================================================
    STADIUM_NAME: str = "FIFA World Cup Arena"

    TOTAL_ZONES: int = 20
    TOTAL_GATES: int = 8
    TOTAL_VOLUNTEERS: int = 200
    MAX_FANS: int = 50000

    # =====================================================
    # SIMULATION
    # =====================================================
    SIMULATION_INTERVAL: float = 1.0
    CROWD_UPDATE_RATE: float = 1.0

    # =====================================================
    # PREDICTION
    # =====================================================
    PREDICTION_WINDOW_MINUTES: int = 10

    CONGESTION_THRESHOLD: float = 0.70
    HIGH_RISK_THRESHOLD: float = 0.90

    # =====================================================
    # WEBSOCKET
    # =====================================================
    WS_UPDATE_INTERVAL: float = 1.0
    MAX_WS_CONNECTIONS: int = 500


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    The .env file is loaded only once for the lifetime
    of the application.
    """
    return Settings()


settings = get_settings()


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("stadiumos")