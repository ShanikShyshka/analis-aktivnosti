from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db, get_analytics_filters
from fastapi import Depends, APIRouter
from typing import List
import schemas
import models as md


router = APIRouter(
    prefix="/api/analytics/rfm",
    tags=["RFM-аналитика"]
)

"""
    :param filters: Словарь с параметрами фильтрации (date_from, date_to, store_id)
    :param db: Асинхронная сессия базы данных AsyncSession
    :param query: SQL-запрос для получения данных RFM-сегментации из md.rfm_analysis
    :param result: Результат выполнения SQL-запроса из базы данных
    :return: Список объектов с оценками Recency, Frequency, Monetary для клиентов
"""


@router.get("", response_model=List[schemas.RFM])
async def get_rfm_analysis(filters: dict = Depends(get_analytics_filters), db: AsyncSession = Depends(get_db)):
    query = select(md.rfm_analysis)
    result = await db.execute(query)

    return result.scalars().all()