import logging

class LoggerSetup:

    logger = logging.getLogger(__name__)

    @staticmethod
    def setup_logging() -> None:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO
        )
        logging.getLogger("httpx").setLevel(logging.WARNING)
        LoggerSetup.logger.info("Logging from setup_logging")