from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Date, Numeric, DateTime
from database import Base
from datetime import date, datetime
from typing import List


class revenue_store(Base):
    __tablename__ = "revenue_stores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    response_id: Mapped[int] = mapped_column(ForeignKey("revenue_responses.id", ondelete="CASCADE"), index=True)
    store_id: Mapped[int] = mapped_column(index=True)
    store_name: Mapped[str] = mapped_column(String(255))
    revenue: Mapped[float] = mapped_column()
    order_count: Mapped[int] = mapped_column()

    response: Mapped["revenue_store_response"] = relationship(back_populates="stores")

class revenue_store_response(Base):
    __tablename__ = "revenue_responses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date_from: Mapped[date] = mapped_column(Date, index=True)
    date_to: Mapped[date] = mapped_column(Date, index=True)
    total_revenue: Mapped[float] = mapped_column(Numeric(15, 2))
    total_orders: Mapped[int] = mapped_column()

    stores: Mapped[List["revenue_store"]] = relationship(back_populates="response", cascade="all, delete-orphan")


class Avg_check_detail(Base):
    __tablename__ = "avg_check_details"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    response_id: Mapped[int] = mapped_column(ForeignKey("avg_check_responses.id", ondelete="CASCADE"), index=True)
    type: Mapped[str] = mapped_column(String(50), index=True)
    text: Mapped[str] = mapped_column(String(255))
    avg_check: Mapped[float] = mapped_column(Numeric(15, 2))
    order_count: Mapped[int] = mapped_column()

    response: Mapped["Avg_check_response"] = relationship(back_populates="details")


class Avg_check_response(Base):
    __tablename__ = "avg_check_responses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    global_avg_check: Mapped[float] = mapped_column(Numeric(15, 2))

    details: Mapped[List["Avg_check_detail"]] = relationship(back_populates="response", cascade="all, delete-orphan")



class product_items(Base):
    __tablename__ = "product_items"

    product_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_name: Mapped[str] = mapped_column(String(255), index=True)
    quantity_sold: Mapped[int] = mapped_column()
    revenue: Mapped[float] = mapped_column(Numeric(15, 2))

class customer_activities(Base):
    __tablename__ = "customer_activities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    customer_count: Mapped[int] = mapped_column()

class rfm_analysis(Base):
    __tablename__ = "rfm_analysis"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_segment: Mapped[str] = mapped_column(String(100), index=True)
    customer_count: Mapped[int] = mapped_column()
    share_percentage: Mapped[float] = mapped_column(Numeric(15, 2))