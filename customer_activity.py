from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, DateTime, cast, func
from database import get_db
from fastapi import Depends, APIRouter, Query
from typing import List, Literal
import schemas
import models as md

router = APIRouter(
    prefix="/api/analytics/customer-activity",
    tags=["Покупательская активность"]
)

"""
    :param group_by: Шаг группировки времени (по дням 'day' или по часам 'hour')
    :param filters: Словарь с параметрами фильтрации (date_from, date_to, store_id)
    :param db: Асинхронная сессия базы данных AsyncSession
    :param trunc_format: Строковый формат для функции date_trunc в SQL
    :param ts_column: Колонка временной метки, приведенная к типу DateTime
    :param query: SQL-запрос со сложной агрегацией (sum, group_by, order_by) по времени
    :param result: Результат выполнения агрегационного SQL-запроса
    :return: Список словарей с отформатированным временем и количеством покупателей
"""


@router.get("", response_model=List[schemas.customer_activities], tags=["Покупательская активность"])

async def get_customer_activity(
        group_by: Literal["day", "hour"] = Query(default="day", description="Группировка: day или hour"),
        db: AsyncSession = Depends(get_db)
):
    ts_column = cast(md.customer_activities.timestamp, DateTime)


    if group_by == "hour":
        group_expr = func.DATE_FORMAT(ts_column, "%Y-%m-%d %H:%i")
    else:  # "day"
        group_expr = func.DATE_FORMAT(ts_column, "%Y-%m-%d 00:00")

    query = (
        select(
            group_expr.label("timestamp"),
            func.sum(md.customer_activities.customer_count).label("customer_count")
        )
        .group_by(group_expr)
        .order_by(group_expr)
    )

    result = await db.execute(query)
    return [{"timestamp": row.timestamp, "customer_count": row.customer_count} for row in result.mappings().all()]
