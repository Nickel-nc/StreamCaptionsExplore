import hashlib
from urllib.parse import urlparse


def url_validator(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


def get_hash(value: str) -> str:
    return hashlib.md5(value.encode("utf-8")).hexdigest()
