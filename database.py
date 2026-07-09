import os
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase




DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/database")


engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    pool_size=10,
    max_overflow=20
)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()  # Автоматический коммит при успешном завершении запроса
        except Exception:
            await session.rollback()  # Откат изменений при возникновении ошибки
            raise
        finally:
            await session.close()  # Гарантированное закрытие сессии
