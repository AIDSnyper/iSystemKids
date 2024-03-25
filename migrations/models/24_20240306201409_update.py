from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "homework" ADD "lesson_id" INT NOT NULL;
        ALTER TABLE "lesson" ADD "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "lesson" ADD "start_date" DATE NOT NULL;
        ALTER TABLE "lesson" ADD "end_date" DATE NOT NULL;
        ALTER TABLE "lesson" ADD "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "homework" ADD CONSTRAINT "fk_homework_lesson_26a781f2" FOREIGN KEY ("lesson_id") REFERENCES "lesson" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "homework" DROP CONSTRAINT "fk_homework_lesson_26a781f2";
        ALTER TABLE "lesson" DROP COLUMN "created_at";
        ALTER TABLE "lesson" DROP COLUMN "start_date";
        ALTER TABLE "lesson" DROP COLUMN "end_date";
        ALTER TABLE "lesson" DROP COLUMN "updated_at";
        ALTER TABLE "homework" DROP COLUMN "lesson_id";"""
