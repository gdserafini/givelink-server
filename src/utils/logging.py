import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - Log: %(message)s"
)


logger = logging.getLogger(__name__)
