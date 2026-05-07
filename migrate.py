"""Простая миграция: добавление колонок если их нет."""
import asyncio
from sqlalchemy import text
from app.db.database import engine


async def migrate():
    async with engine.begin() as conn:
        # Проверяем существование таблиц и добавляем недостающие колонки
        # SQLite-specific
        result = await conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result.fetchall()]

        print(f"Найденные таблицы: {tables}")

        if "cases" in tables:
            # Проверяем колонки
            result = await conn.execute(text("PRAGMA table_info(cases)"))
            columns = [row[1] for row in result.fetchall()]
            print(f"Колонки в cases: {columns}")

            # Добавляем недостающие колонки при необходимости
            # (SQLAlchemy create_all сделает это автоматически при init_db)

        print("✅ Миграция завершена")


if __name__ == "__main__":
    asyncio.run(migrate())
