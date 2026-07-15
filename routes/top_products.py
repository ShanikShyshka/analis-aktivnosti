from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from database import get_db, get_analytics_filters
from fastapi import Depends, APIRouter, Query
from typing import List, Literal
import schemas
import models as md

router = APIRouter(
    prefix="/api/analytics/top-products",
    tags=["Топ продуктов"]
)

"""
    :param limit: Ограничение на количество возвращаемых товаров в топе (от 1 до 50)
    :param sort_by: Критерий сортировки топа (по количеству 'quantity' или выручке 'revenue')
    :param filters: Словарь с параметрами фильтрации (date_from, date_to, store_id)
    :param db: Асинхронная сессия базы данных AsyncSession
    :param sort_column: Колонка модели md.product_items, по которой будет идти сортировка
    :param query: SQL-запрос для выборки товаров с сортировкой и лимитом
    :param result: Результат выполнения SQL-запроса из базы данных
    :return: Список объектов самых продаваемых товаров
"""

@router.get("", response_model=List[schemas.product_item], tags=["Топ продуктов"])
async def get_top_products(
        limit: int = Query(default=10, ge=1, le=50, description="Количество товаров в топе"),
        sort_by: Literal["quantity", "revenue"] = Query(default="quantity",
                                                        description="Сортировать по: quantity или revenue"),
        db: AsyncSession = Depends(get_db)
):
    sort_column = md.product_items.quantity_sold if sort_by == "quantity" else md.product_items.revenue

    query = select(md.product_items).order_by(desc(sort_column)).limit(limit)
    result = await db.execute(query)

    return result.scalars().all()
