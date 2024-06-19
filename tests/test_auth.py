import pytest
from sqlalchemy import insert, select
from src.auth.models import Role, User
from conftest import client, async_session_maker
import logging

logger = logging.getLogger(__name__)


async def test_add_role():
    logger.info("Starting test_add_role...")
    async with async_session_maker() as session:
        stmt = insert(Role).values(id=1, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(Role)
        result = await session.execute(query)
        roles = result.all()
        logger.info(f"Roles in database: {roles}")
        assert roles == [(1, "admin", None)], "Роль не добавилась"


def test_register():
    logger.info("Starting test_register...")
    response = client.post("/auth/register", json={
        "email": "string12132121@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "role_id": 1
    })
    logger.info(f"Register response: {response.json()}")
    assert response.status_code == 201, response.text
