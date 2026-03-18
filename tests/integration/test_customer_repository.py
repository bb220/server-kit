import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from server_kit.db.session import create_session_factory
from server_kit.repositories import CustomerRepository
from server_kit.schemas import CustomerCreate, CustomerUpdate
from tests.support.database import (
    create_test_engine,
    run_alembic_upgrade,
    temporary_database,
)


@pytest.mark.anyio
async def test_customer_repository_crud_operations():
    async with temporary_database("server_kit_customer_repo") as database_url:
        run_alembic_upgrade(database_url)
        engine = create_test_engine(database_url)
        session_factory: async_sessionmaker = create_session_factory(engine)

        try:
            async with session_factory() as session:
                repository = CustomerRepository(session)

                created = await repository.create(
                    CustomerCreate(name="Jane Doe", city="Boston", state="MA")
                )
                await session.commit()

                fetched = await repository.get_by_id(created.id)
                assert fetched is not None
                assert fetched.name == "Jane Doe"

                updated = await repository.update(
                    fetched,
                    CustomerUpdate(city="Providence"),
                )
                await session.commit()

                assert updated.city == "Providence"
                assert updated.state == "MA"

                customers = await repository.list(limit=10, offset=0)
                assert len(customers) == 1
                assert customers[0].id == created.id

                await repository.delete(updated)
                await session.commit()

                assert await repository.get_by_id(created.id) is None
        finally:
            await engine.dispose()
