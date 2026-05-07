"""Скрипт для начального заполнения базы данных."""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal, init_db
from app.models.models import TeamLead, ScriptTemplate


TEAMLEADS = [
    {"name": "Дмитрий Юрнюк", "direction": "Инфлюенс"},
    {"name": "Владилен Гутов", "direction": "SERM и ORM"},
    {"name": "Денис Соболев", "direction": "Масскомментинг на YouTube"},
    {"name": "Ольга Лонн", "direction": "Лидогенерация"},
    {"name": "Александра Можаева", "direction": "Медиабустер"},
    {"name": "Мария Дудина", "direction": "Перформанс"},
    {"name": "Полина Тихонова", "direction": "Перформанс"},
    {"name": "Полина Сидельникова", "direction": "Market Research"},
    {"name": "Полина Сидельникова", "direction": "PMO"},
]

DEFAULT_TEMPLATES = [
    {
        "name": "medium_description",
        "template_text": """Кейс для {client_name}: {product_description}. 
Цель: {goal}. Результаты: {results}. Ключевые метрики: {metrics}."""
    },
    {
        "name": "short_description",
        "template_text": """{product_description} — {results}"""
    },
]


async def seed_teamleads(session: AsyncSession):
    for data in TEAMLEADS:
        teamlead = TeamLead(**data)
        session.add(teamlead)
    await session.commit()
    print(f"✅ Добавлено {len(TEAMLEADS)} тимлидов")


async def seed_templates(session: AsyncSession):
    for data in DEFAULT_TEMPLATES:
        template = ScriptTemplate(**data)
        session.add(template)
    await session.commit()
    print(f"✅ Добавлено {len(DEFAULT_TEMPLATES)} шаблонов")


async def main():
    await init_db()
    async with AsyncSessionLocal() as session:
        await seed_teamleads(session)
        await seed_templates(session)
    print("🎉 База данных заполнена!")


if __name__ == "__main__":
    asyncio.run(main())
