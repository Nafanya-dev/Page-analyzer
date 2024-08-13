from validators.url import url as url_validator
from urllib.parse import urlparse

MAX_LENGTH_URL = 255


def normalize_url(url):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc
    normalized_url = f"{scheme}://{netloc}".lower()
    return normalized_url


def validate(url):
    errors = {}
    if not url_validator(url):
        errors['message'] = 'Некорректный URL'
    else:
        if len(url) > MAX_LENGTH_URL:
            errors['message'] = 'URL превышает 255 символов'
    return errors
