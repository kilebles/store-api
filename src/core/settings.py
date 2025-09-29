from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_URL:str

    PGADMIN_EMAIL: str
    PGADMIN_PASSWORD: str

    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_BUCKET: str

    CORS_ORIGINS: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        if not self.CORS_ORIGINS:
            return []
        return [s.strip() for s in self.CORS_ORIGINS.split(",") if s.strip()]

    model_config = {"env_file": ".env"}