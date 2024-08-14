import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
from .models import Url


def get_connection(data_base):
    return psycopg2.connect(data_base)


def commit(conn):
    conn.commit()


def save_url(url, database):
    sql = "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;"
    with get_connection(database) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            current_time = datetime.now().date()
            cur.execute(sql, (url.name, current_time))
            url.id = cur.fetchone()['id']
            url.created_at = current_time
            commit(conn)


def check_url(id_, database):
    sql = """
        INSERT INTO url_checks (url_id, created_at)
        VALUES (%s, %s);
        """
    with get_connection(database) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            current_time = datetime.now().date()
            cur.execute(sql, (id_, current_time))
            commit(conn)


def get_id(name, database):
    sql = "SELECT id FROM urls WHERE name = %s;"
    with get_connection(database) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql, (name,))
            result = cur.fetchone()
            commit(conn)
            return result['id'] if result else None


def get_url(id_, database):
    sql = """
        SELECT id, name, created_at
        FROM urls
        WHERE id = %s
        """
    with get_connection(database) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql, (id_,))
            result = cur.fetchone()
            commit(conn)
            return Url(**result)


def get_all_urls(database):
    sql = """
        SELECT urls.id, urls.name, url_checks.created_at
        FROM urls
        LEFT JOIN url_checks ON urls.id = url_checks.url_id
        WHERE url_checks.url_id IS NULL OR
        url_checks.id = (SELECT MAX(url_checks.id)
        FROM url_checks
        WHERE url_checks.url_id = urls.id)
        ORDER BY urls.id DESC;
        """
    with get_connection(database) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql)
            result = cur.fetchall()
            commit(conn)
            return result


def get_checked_urls(url, database):
    sql = """
        SELECT id, created_at
        FROM url_checks
        WHERE url_id = %s
        ORDER BY id DESC;
        """
    with get_connection(database) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql, (url.id,))
            result = cur.fetchall()
            commit(conn)
            return result if result else []