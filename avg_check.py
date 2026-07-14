from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db, get_analytics_filters
from fastapi import Depends, APIRouter
import schemas
import models as md


router = APIRouter(
    prefix="/api/analytics/avg-check",
    tags=["Средний чек"]
)


"""
    :param filters: Словарь с параметрами фильтрации (date_from, date_to, store_id)
    :param db: Асинхронная сессия базы данных AsyncSession
    :param store_query: SQL-запрос для получения среднего чека в разрезе магазинов
    :param hour_query: SQL-запрос для получения среднего чека в разрезе часов суток
    :param store_result: Результат выполнения SQL-запроса по магазинам
    :param hour_result: Результат выполнения SQL-запроса по часам
    :param check_by_store: Список объектов со средним чеком по каждому магазину
    :param check_by_hour: Список объектов со средним чеком по часам суток
    :param total_revenue: Общая выручка, рассчитанная для вычисления глобального среднего чека
    :param total_orders: Общее количество заказов для вычисления глобального среднего чека
    :param global_avg: Итоговый средний чек по всей сети (округленный до 2 знаков)
    :return: Словарь с общим средним чеком и детализацией по магазинам и часам
"""

@router.get("", response_model=schemas.avg_check_response, tags=["Средний чек"])
async def get_avg_check(filters: dict = Depends(get_analytics_filters), db: AsyncSession = Depends(get_db)):
    store_query = select(md.Avg_check_detail).where(md.Avg_check_detail.type == "store")

    if filters["store_id"] is not None:
        store_query = store_query.where(md.Avg_check_detail.text == select(md.revenue_store.store_id).where(
            md.revenue_store.store_id == filters["store_id"]).scalar_subquery())

    hour_query = select(md.Avg_check_detail).where(md.Avg_check_detail.type == "hour")

    store_result = await db.execute(store_query)
    hour_result = await db.execute(hour_query)

    check_by_store = store_result.scalars().all()
    check_by_hour = hour_result.scalars().all()

    total_revenue = sum(item.avg_check * item.order_count for item in check_by_store)
    total_orders = sum(item.order_count for item in check_by_store)
    global_avg = round(total_revenue / total_orders, 2) if total_orders > 0 else 0.0

    return {
        "global_avg_check": global_avg,
        "check_by_store": check_by_store,
        "check_by_hour": check_by_hour
    }