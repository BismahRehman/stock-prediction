#
# from app.database import engine
# from tests.config import settings
#
# TEST_DATABASE_URL= settings.DATABASE_URL
#
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker, declarative_base
#
# engine = create_async_engine(TEST_DATABASE_URI = settings.DATABASE_URI, echo=True)
# TestingAsyncSessionLocal = sessionmaker(
#                 bind=engine,
#                 class_=AsyncSession,
#                 expire_on_commit=False
# )
#
# Base = declarative_base()
#
