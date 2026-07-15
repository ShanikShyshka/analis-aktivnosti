from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import get_db, get_analytics_filters
import models as md

router = APIRouter(
    prefix="/api/analytics/revenue",
    tags=["Выручка"]
)

"""
Получить ежедневную аналитику выручки и заказов с фильтрацией по датам.

Возвращает агрегированные данные о выручке и количестве заказов по дням,
а также общие суммарные показатели за весь указанный период.

:param filters: Словарь параметров фильтрации (date_from, date_to, store_id).
:param db: Асинхронная сессия SQLAlchemy (AsyncSession) для работы с БД.
:return: Словарь, содержащий общую выручку (total_revenue), общее число заказов
         (total_orders) и список с разбивкой по дням (daily_data).
"""

@router.get("")
async def get_revenue(
    filters: dict = Depends(get_analytics_filters),
    db: AsyncSession = Depends(get_db)
):
    # 1. Основной запрос с явным JOIN между avg_check_details и avg_check_responses
    daily_query = (
        select(
            md.Avg_check_detail.response_id,
            func.sum(md.Avg_check_detail.avg_check * md.Avg_check_detail.order_count).label('daily_revenue'),
            func.sum(md.Avg_check_detail.order_count).label('daily_orders'),
            md.Avg_check_response.date.label('date')
        )
        .select_from(md.Avg_check_detail)
        .join(md.Avg_check_response, md.Avg_check_detail.response_id == md.Avg_check_response.id)
        .where(
            md.Avg_check_detail.type == 'store',
            md.Avg_check_response.date >= filters['date_from'],
            md.Avg_check_response.date <= filters['date_to']
        )
        .group_by(md.Avg_check_detail.response_id, md.Avg_check_response.date)
        .order_by(md.Avg_check_response.date)
    )

    result = await db.execute(daily_query)
    rows = result.all()

    daily_data = []
    total_revenue = 0
    total_orders = 0

    for row in rows:
        daily_data.append({
            'date': row.date.isoformat(),
            'revenue': float(row.daily_revenue),
            'orders': int(row.daily_orders)
        })
        total_revenue += float(row.daily_revenue)
        total_orders += int(row.daily_orders)

    return {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'daily_data': daily_data
    }