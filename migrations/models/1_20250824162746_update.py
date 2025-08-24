from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `meeting` ADD `location` VARCHAR(255) NOT NULL  DEFAULT '';
        ALTER TABLE `meeting` ADD `end_date` DATE;
        ALTER TABLE `meeting` ADD `start_date` DATE;
        ALTER TABLE `meeting` ADD `title` VARCHAR(255) NOT NULL  DEFAULT '';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `meeting` DROP COLUMN `location`;
        ALTER TABLE `meeting` DROP COLUMN `end_date`;
        ALTER TABLE `meeting` DROP COLUMN `start_date`;
        ALTER TABLE `meeting` DROP COLUMN `title`;"""
