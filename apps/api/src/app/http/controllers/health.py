from litestar import Controller, get
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class HealthController(Controller):
    path = "/health"

    @get()
    async def healthcheck(self) -> dict[str, str]:
        return {"status": "ok"}

    @get("/db")
    async def db_healthcheck(self, db_session: AsyncSession) -> dict[str, str]:
        result = await db_session.execute(text("SELECT 1"))
        value = result.scalar_one()

        return {"status": "ok", "db": "ok" if value == 1 else "unexpected"}
