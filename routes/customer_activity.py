from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, DateTime, cast, func
from database import get_db, get_analytics_filters
from fastapi import Depends, APIRouter, Query
from typing import List, Literal
import schemas
import models as md

router = APIRouter(
    prefix="/api/analytics/customer-activity",
    tags=["Покупательская активность"]
)

"""
Получить агрегированную покупательскую активность с фильтрацией по датам.

Возвращает временной ряд с количеством покупателей, сгруппированный 
по дням или часам в рамках указанного периода.

:param group_by: Тип группировки данных ("day" для дней, "hour" для часов).
:param filters: Словарь параметров фильтрации (date_from, date_to, store_id).
:param db: Асинхронная сессия SQLAlchemy (AsyncSession) для работы с БД.
:return: Список словарей/объектов, содержащих сгруппированную дату (timestamp) 
         и суммарное количество покупателей (customer_count).
"""


@router.get("", response_model=List[schemas.customer_activities])
async def get_customer_activity(
        group_by: Literal["day", "hour"] = Query(default="day", description="Группировка: day или hour"),
        filters: dict = Depends(get_analytics_filters),
        db: AsyncSession = Depends(get_db)
):
    ts_column = cast(md.customer_activities.timestamp, DateTime)

    if group_by == "hour":
        group_expr = func.DATE_FORMAT(ts_column, "%Y-%m-%d %H:00:00")
    else:
        group_expr = func.DATE_FORMAT(ts_column, "%Y-%m-%d 00:00:00")

    group_expr = cast(group_expr, DateTime)

    query = (
        select(
            group_expr.label("timestamp"),
            func.sum(md.customer_activities.customer_count).label("customer_count")
        )
        .where(
            md.customer_activities.timestamp >= filters["date_from"],
            md.customer_activities.timestamp <= filters["date_to"]
        )
        .group_by(group_expr)
        .order_by(group_expr)
    )

    result = await db.execute(query)
    return result.mappings().all()