import logging
import sys
from app.config import get_settings

settings = get_settings()

# Create logger
logger = logging.getLogger("pod_trends")
logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)

# Console handler
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

export = logger
