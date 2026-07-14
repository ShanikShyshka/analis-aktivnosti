from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from fastapi import Query
from datetime import date, timedelta, datetime



DATABASE_URL = "mysql+aiomysql://root:12345@localhost:3306/database"


engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    pool_size=10,
    max_overflow=20
)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session = async_session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()



"""
    :param dateFrom: Начало периода (по умолчанию: 30 дней назад).
    :param dateTO: Конец периода (по умолчанию: сегодня).
    :param storeID: ID конкретного магазина. Если не передан, данные собираются по всей торговой сети
    :return: Возвращает параметры фильтра
"""

def get_analytics_filters(
        dateFrom: date = Query(default=date.today() - timedelta(days=30), description="Начало периода"),
        dateTo: date = Query(default=date.today(), description="Конец периода"),
        storeId: Optional[int] = Query(default=None, description="ID магазина для фильтрации (опционально)")
):
    return {"date_from": dateFrom, "date_to": dateTo, "store_id": storeId}