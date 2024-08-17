import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
from .models import Url, UrlCheck
from .config import DATABASE_URL
from typing import Optional


DATABASE: Optional[str] = DATABASE_URL


def get_connection(data_base: str):
    """
    Устанавливает соединение с базой данных.
    """
    return psycopg2.connect(data_base)


def save_url(url: Url) -> None:
    """
    Добавляет Url в базу данных в таблицу urls.
    """
    sql = "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;"
    with get_connection(DATABASE) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            current_time = datetime.now().date()
            cur.execute(sql, (url.name, current_time))
            url.id = cur.fetchone().get("id")
            url.created_at = current_time


def add_checked_url(url: Url, url_checked: UrlCheck) -> None:
    """
    Сохраняет проверенный Url в базу данных
    в таблицу url_checks.
    """
    sql = """
        INSERT INTO url_checks (url_id,
        status_code, created_at, h1,
        title, description)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
    with get_connection(DATABASE) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql, (url.id,
                              url_checked.status_code,
                              url_checked.created_at,
                              url_checked.h1,
                              url_checked.title,
                              url_checked.description))


def get_id(name: str) -> Optional[int]:
    """
    Получает Идентификатор (id) конкретного url по заданному имени (name)
    из базы данных в таблице urls.

    :return:
    Идентификатор URL, если он существует в базе данных;
    None, если URL с таким именем не найден.
    """
    sql = "SELECT id FROM urls WHERE name = %s;"
    with get_connection(DATABASE) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql, (name,))
            result = cur.fetchone()
            return result.get("id") if result is not None else None


def get_url(id_: id) -> Url:
    """
    Получает URL по его идентификатору (id_).

    :return:
    Объект Url, если найден; None, если не найден.
    """
    sql = """
        SELECT id, name, created_at
        FROM urls
        WHERE id = %s
        """
    with get_connection(DATABASE) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql, (id_,))
            result = cur.fetchone()
            return Url(**result)


def get_all_urls() -> list:
    """
    Получает все URL с последними проверками.

    :return:
    Список словарей с информацией о URL и их последнем статусе.
    """
    sql = """
        SELECT urls.id, urls.name,
        url_checks.created_at, url_checks.status_code
        FROM urls
        LEFT JOIN url_checks ON urls.id = url_checks.url_id
        WHERE url_checks.url_id IS NULL OR
        url_checks.id = (SELECT MAX(url_checks.id)
        FROM url_checks
        WHERE url_checks.url_id = urls.id)
        ORDER BY urls.id DESC;
        """
    with get_connection(DATABASE) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql)
            result = cur.fetchall()
            return result


def get_checked_urls(url: Url) -> list:
    """
    Получает все проверки для заданного URL.

    :return:
    Список словарей с информацией о проверках URL.
    """
    sql = """
        SELECT id, status_code, h1, title, description, created_at
        FROM url_checks
        WHERE url_id = %s
        ORDER BY id DESC;
        """
    with get_connection(DATABASE) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql, (url.id,))
            result = cur.fetchall()
            return result if result else []
