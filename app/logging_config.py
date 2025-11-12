import logging
import re


def mask_sensitive_data(message: str) -> str:
    patterns = [
        (r'password["\']?\s*[:=]\s*["\']?([^"\'\s]+)', r'password="***"'),
        (r'token["\']?\s*[:=]\s*["\']?([^"\'\s]+)', r'token="***"'),
        (r'api[_-]?key["\']?\s*[:=]\s*["\']?([^"\'\s]+)', r'api_key="***"'),
        (r'secret["\']?\s*[:=]\s*["\']?([^"\'\s]+)', r'secret="***"'),
        (r'email["\']?\s*[:=]\s*["\']?([^"\'\s@]+@[^"\'\s]+)', r'email="***@***"'),
    ]

    for pattern, replacement in patterns:
        message = re.sub(pattern, replacement, message, flags=re.IGNORECASE)

    return message


class SafeFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        original_msg = record.getMessage()
        masked_msg = mask_sensitive_data(original_msg)
        record.msg = masked_msg
        record.args = ()
        return super().format(record)


def setup_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(
        SafeFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False

    return logger
