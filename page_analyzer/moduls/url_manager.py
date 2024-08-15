from validators.url import url as url_validator
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse
from .models import UrlCheck
import requests

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


def check_url(url):
    try:
        with (requests.get(url.name) as r):
            r.raise_for_status()

            html_content = r.text
            soup = BeautifulSoup(html_content, 'html.parser')

            status_code = r.status_code
            h1 = soup.h1.text if soup.h1 else None
            title = soup.title.text if soup.title else None
            meta_description = soup.find('meta', attrs={'name': 'description'})
            description = meta_description.get('content'
                                               )if meta_description else None
            current_time = datetime.now().date()
            return UrlCheck(status_code=status_code,
                            h1=h1,
                            title=title,
                            description=description,
                            created_at=current_time
                            )
    except requests.exceptions.RequestException:
        return None
