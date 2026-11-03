import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:subodhnepal10@localhost:5432/dbname")


engine = create_async_engine(
    DATABASE_URL,
    echo=False,          
    pool_pre_ping=True,  
    pool_size=10,        
    max_overflow=20      
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  
    autocommit=False,
    autoflush=False
)


Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
            
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
