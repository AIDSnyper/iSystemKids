from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "homeworks" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(44) NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL,
    "file" VARCHAR(255) NOT NULL,
    "mark" INT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "lesson" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "content" TEXT NOT NULL,
    "students" VARCHAR(255),
    "teacher" VARCHAR(44)
);
CREATE TABLE IF NOT EXISTS "shop" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(44) NOT NULL,
    "price_tokens" INT NOT NULL,
    "price_diamonds" INT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "usermodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(44) NOT NULL UNIQUE,
    "name" VARCHAR(44) NOT NULL,
    "last_name" VARCHAR(44) NOT NULL,
    "email" VARCHAR(44) NOT NULL,
    "role" VARCHAR(44) NOT NULL,
    "balance_diamonds" INT NOT NULL  DEFAULT 0,
    "balance_tokens" INT NOT NULL  DEFAULT 0,
    "avatar" VARCHAR(404),
    "password" VARCHAR(404) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
