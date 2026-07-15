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
Получить аналитику среднего чека в сети магазинов.

Возвращает глобальный средний чек, рассчитанный на основе переданных фильтров,
а также детализированную информацию в разрезе магазинов и часов суток.


    :param filters: Словарь с параметрами фильтрации (date_from, date_to, store_id)
    :param db: Асинхронная сессия базы данных AsyncSession
    :param store_query: SQL-запрос для получения среднего чека в разрезе магазинов
    :param hour_query: SQL-запрос для получения среднего чека в разрезе часов суток
    :param store_result: Результат выполнения SQL-запроса по магазинам
    :param day_result: Результат выполнения SQL-запроса по часам
    :param check_by_store: Список объектов со средним чеком по каждому магазину
    :param check_by_hour: Список объектов со средним чеком по часам суток
    :param total_revenue: Общая выручка, рассчитанная для вычисления глобального среднего чека
    :param total_orders: Общее количество заказов для вычисления глобального среднего чека
    :param global_avg: Итоговый средний чек по всей сети (округленный до 2 знаков)
    :return: Словарь с общим средним чеком и детализацией по магазинам и часам
"""






@router.get("", response_model=schemas.avg_check_response)
async def get_avg_check(
    filters: dict = Depends(get_analytics_filters),
    db: AsyncSession = Depends(get_db)
):
    # 1. Запрос для store-агрегатов (по магазинам) – без фильтрации по дате
    store_query = select(md.Avg_check_detail).where(
        md.Avg_check_detail.type == "store"
    )
    if filters.get("store_id") is not None:
        store_query = store_query.where(
            md.Avg_check_detail.text == select(md.revenue_store.store_id).where(
                md.revenue_store.store_id == filters["store_id"]
            ).scalar_subquery()
        )

    # 2. Запрос для day-агрегатов (по дням) – фильтруем по дате через поле text
    #    Предполагается, что в таблице avg_check_details есть записи с type='day',
    #    где text содержит дату в формате 'YYYY-MM-DD'
    day_query = select(md.Avg_check_detail).where(
        md.Avg_check_detail.type == "day",
        md.Avg_check_detail.text >= filters["date_from"],
        md.Avg_check_detail.text <= filters["date_to"]
    )

    store_result = await db.execute(store_query)
    day_result = await db.execute(day_query)

    check_by_store = store_result.scalars().all()
    check_by_day = day_result.scalars().all()

    def to_dict(item):
        return {
            "id": item.id,
            "text": item.text,
            "avg_check": item.avg_check,
            "order_count": item.order_count,
        }

    check_by_store_dicts = [to_dict(item) for item in check_by_store]
    check_by_day_dicts = [to_dict(item) for item in check_by_day]

    total_revenue = sum(item.avg_check * item.order_count for item in check_by_store)
    total_orders = sum(item.order_count for item in check_by_store)
    global_avg = round(total_revenue / total_orders, 2) if total_orders > 0 else 0.0

    return {
        "global_avg_check": global_avg,
        "check_by_store": check_by_store_dicts,
        "check_by_hour": check_by_day_dicts,
    }