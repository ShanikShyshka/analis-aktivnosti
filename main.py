from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, Base

from routes import revenue, rfm, avg_check, customer_activity,top_products

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

app.include_router(revenue.router)
app.include_router(rfm.router)
app.include_router(avg_check.router)
app.include_router(customer_activity.router)
app.include_router(top_products.router)









