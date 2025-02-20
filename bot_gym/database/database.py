import asyncpg

async def create_db_pool(PG_HOST, PG_USER, PG_PASSWORD, PG_DATABASE):
    pool = await asyncpg.create_pool(
        host=PG_HOST,
        user=PG_USER,
        password=PG_PASSWORD,
        database=PG_DATABASE,
    )
    return pool