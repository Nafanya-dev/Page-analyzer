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


def is_there_url(url, database):
    sql = "SELECT id FROM urls WHERE name = %s;"
    with get_connection(database) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql, (url.name,))
            result = cur.fetchone()
            commit(conn)
            if result:
                url.id = result['id']
                return True
        return False


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
        SELECT *
        FROM urls
        ORDER BY id DESC;
        """
    with get_connection(database) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql)
            result = cur.fetchall()
            commit(conn)
    return result
