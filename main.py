from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta
from typing import List, Optional, Literal
from sqlalchemy import select, func, desc, cast, DateTime

import schemas
from database import engine, Base, get_db

import models as md


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Analytics API",
    description="REST API для дашборда аналитики торговой сети",
    version="1.0.0",
    lifespan=lifespan
)
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
@app.get("/api/analytics/revenue", response_model=schemas.revenue_store_response, tags=["Выручка"])
async def get_revenue(filters: dict = Depends(get_analytics_filters), db: AsyncSession = Depends(get_db)):
    # Используем корректные классы моделей md.revenue_store и md.revenue_store_response
    query = select(md.revenue_store).join(md.revenue_store_response).where(
        md.revenue_store_response.date_from >= str(filters["date_from"]),
        md.revenue_store_response.date_to <= str(filters["date_to"])
    )

    if filters["store_id"] is not None:
        query = query.where(md.revenue_store.store_id == filters["store_id"])

    result = await db.execute(query)
    stores = result.scalars().all()

    total_revenue = sum(store.revenue for store in stores)
    # ВНИМАНИЕ: Убедитесь, что добавили order_count в md.revenue_store, иначе тут будет AttributeError
    total_orders = sum(getattr(store, "order_count", 0) for store in stores)

    return {
        "date_from": filters["date_from"],
        "date_to": filters["date_to"],
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "stores": stores
    }

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

@app.get("/api/analytics/avg-check", response_model=schemas.avg_check_response, tags=["Средний чек"])
async def get_avg_check(filters: dict = Depends(get_analytics_filters), db: AsyncSession = Depends(get_db)):
    store_query = select(md.Avg_check_detail).where(md.Avg_check_detail.type == "store")

    if filters["store_id"] is not None:
        store_query = store_query.where(md.Avg_check_detail.text == select(md.revenue_store.store_name).where(
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


@app.get("/api/analytics/top-products", response_model=List[schemas.product_item], tags=["Топ продуктов"])
async def get_top_products(
        limit: int = Query(default=10, ge=1, le=50, description="Количество товаров в топе"),
        sort_by: Literal["quantity", "revenue"] = Query(default="quantity",
                                                        description="Сортировать по: quantity или revenue"),
        filters: dict = Depends(get_analytics_filters),
        db: AsyncSession = Depends(get_db)
):
    sort_column = md.product_items.quantity_sold if sort_by == "quantity" else md.product_items.revenue

    query = select(md.product_items).order_by(desc(sort_column)).limit(limit)
    result = await db.execute(query)

    return result.scalars().all()


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


@app.get("/api/analytics/customer-activity", response_model=List[schemas.customer_activity],
         tags=["Покупательская активность"])
async def get_customer_activity(
        group_by: Literal["day", "hour"] = Query(default="day", description="Группировка: day или hour"),
        filters: dict = Depends(get_analytics_filters),
        db: AsyncSession = Depends(get_db)
):
    trunc_format = "day" if group_by == "day" else "hour"

    ts_column = cast(md.customer_activities.timestamp, DateTime)

    query = (
        select(
            func.to_char(func.date_trunc(trunc_format, ts_column), 'YYYY-MM-DD HH24:MI').label("timestamp"),
            func.sum(md.customer_activities.customer_count).label("customer_count")
        )
        .group_by(func.date_trunc(trunc_format, ts_column))
        .order_by(func.date_trunc(trunc_format, ts_column))
    )

    result = await db.execute(query)
    return [{"timestamp": row.timestamp, "customer_count": row.customer_count} for row in result.all()]


"""
    :param filters: Словарь с параметрами фильтрации (date_from, date_to, store_id)
    :param db: Асинхронная сессия базы данных AsyncSession
    :param query: SQL-запрос для получения данных RFM-сегментации из md.rfm_analysis
    :param result: Результат выполнения SQL-запроса из базы данных
    :return: Список объектов с оценками Recency, Frequency, Monetary для клиентов
"""


@app.get("/api/analytics/rfm", response_model=List[schemas.RFM], tags=["RFM Аналитика"])
async def get_rfm_analysis(filters: dict = Depends(get_analytics_filters), db: AsyncSession = Depends(get_db)):
    query = select(md.rfm_analysis)
    result = await db.execute(query)

    return result.scalars().all()
