from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List


class revenue_store(BaseModel):
    store_id: int = Field(..., description="ID магазина")
    store_name: str = Field(..., description="Имя магазина")
    revenue: float = Field(..., description="Выручка")
    order_count: int = Field(..., description="Количество заказов")


class revenue_store_response(BaseModel):
    date_from: date = Field()
    date_to: date = Field()
    total_revenue: float = Field()
    total_orders: int = Field()
    stores: List[revenue_store] = Field()



class avg_check_detail(BaseModel):
    text: str = Field(..., description="Название магазина или час дня", alias="Text")
    avg_check: float = Field(..., description="Размер среднего чека")
    order_count: int = Field(..., description="Количество заказов")

    class Config:
        populate_by_name = True

class avg_check_response(BaseModel):
    global_avg_check: float = Field(..., description="Общий средний чек по всей сети")
    check_by_store: List[avg_check_detail] = Field(..., description="Средний чек по магазинам")
    check_by_hour: List[avg_check_detail] = Field(..., description="Средний чек по часам")


class product_item(BaseModel):
    product_id: int
    product_name: str
    quantity_sold: int = Field(..., description="Количество проданого")
    revenue: float = Field(..., description="Выручка")
class customer_activities(BaseModel):
    timestamp: datetime = Field()
    customer_count: int

    class Config:
        from_attributes = True

class RFM(BaseModel):
    customer_segment: str = Field(..., description="Сегменты клиентов")
    customer_count: int = Field(..., description="Количество клиентов в сегменте ")
    share_percentage: float = Field(..., description="Доля сегмента в процентах")

