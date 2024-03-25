from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "homework" DROP CONSTRAINT "fk_homework_lesson_26a781f2";
        ALTER TABLE "homework" ADD "lesson" VARCHAR(222) NOT NULL;
        ALTER TABLE "homework" DROP COLUMN "lesson_id";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "homework" ADD "lesson_id" INT NOT NULL;
        ALTER TABLE "homework" DROP COLUMN "lesson";
        ALTER TABLE "homework" ADD CONSTRAINT "fk_homework_lesson_26a781f2" FOREIGN KEY ("lesson_id") REFERENCES "lesson" ("id") ON DELETE CASCADE;"""
