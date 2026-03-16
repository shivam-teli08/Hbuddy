from __future__ import annotations

import os

from dotenv import load_dotenv


load_dotenv()


def normalize_database_url(url: str) -> str:
    if url.startswith("postgresql://") and "+psycopg" not in url:
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "hbuddy-secret-key")
    SQLALCHEMY_DATABASE_URI = normalize_database_url(
        os.getenv("DATABASE_URL", "postgresql+psycopg://postgres@localhost:5432/hbuddy")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
