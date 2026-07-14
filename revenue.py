from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db, get_analytics_filters
import models as md
import schemas

router = APIRouter(
    prefix="/api/analytics/revenue",
    tags=["Выручка"]
)

"""
    :param date_from:  Дата начала отчета.
    :param date_to: Дата конца отчета.
    :param total_revenue: Суммарная выручка (в валюте) по всем найденным точкам за период.
    :param total_orders: Суммарное количество чеков/заказов за период.
    :stores(list):
        :param store_id: Уникальный номер магазина.
        :param store_name: Название торговой точки.
        :param revenue: Выручка конкретного магазина.
        :param order_count: Количество заказов конкретного магазина
    :return: Считает общую финансовую выручку и количество заказов за указанный период (глобально или по конкретному магазину).
"""

@router.get("", response_model=schemas.revenue_store_response)
async def get_revenue(
    filters: dict = Depends(get_analytics_filters),
    db: AsyncSession = Depends(get_db)
):
    query = select(md.revenue_store).join(md.revenue_store_response).where(
        md.revenue_store_response.date_from >= filters["date_from"],
        md.revenue_store_response.date_to <= filters["date_to"]
    )

    if filters.get("store_id") is not None:
        query = query.where(md.revenue_store.store_id == filters["store_id"])

    result = await db.execute(query)
    stores = result.scalars().all()

    total_revenue = sum(store.revenue for store in stores)
    total_orders = sum(getattr(store, "order_count", 0) for store in stores)

    return {
        "date_from": filters["date_from"],
        "date_to": filters["date_to"],
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "stores": stores
    }
