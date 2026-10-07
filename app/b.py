import os

from sqlalchemy import create_engine, text

_engine = None
_engine_url = None


class DatabaseNotConfigured(Exception):
    pass


def get_engine():
    global _engine, _engine_url
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise DatabaseNotConfigured()
    if _engine is None or url != _engine_url:
        _engine = create_engine(url, pool_pre_ping=True)
        _engine_url = url
    return _engine


def query(sql, params=None):
    with get_engine().connect() as conn:
        result = conn.execute(text(sql), params or {})
        return [dict(row._mapping) for row in result]
