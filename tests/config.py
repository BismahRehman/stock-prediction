# from pydantic_settings import BaseSettings
#
# class Settings(BaseSettings):
#
#     # Database
#     DATABASE_URI: str
#
#     # JWT Token
#     SECRET_KEY: str
#     ALGORITHM: str
#     ACCESS_TOKEN_EXPIRE_MINUTES: int
#
#     # Google OAuth config
#     CLIENT_ID: str
#     CLIENT_SECRET: str
#     REDIRECT_URI: str
#     TOKEN_URL: str
#     USERINFO_URL: str
#
#     # stripe
#     STRIPE_SECRET_KEY : str
#     STRIPE_WEBHOOK_SECRET : str
#     DOMAIN_URL : str
#     PRICE_ID : str
#
#    # admin
#     ADMIN_EMAIL : str
#     ADMIN_PASSWORD : str
#
#
#     class Config:
#         env_file = ".env"
#
# settings = Settings()