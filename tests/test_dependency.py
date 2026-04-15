# from app.dependency import get_db
# from app.main import app
# from tests.test_database import TestingAsyncSessionLocal
#
#
# async def override_get_db():
#
#         async with TestingAsyncSessionLocal() as db:
#             yield db
#
# app.dependency.get_db[get_db] = override_get_db