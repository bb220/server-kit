from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from server_kit.models import Customer
from server_kit.schemas import CustomerCreate, CustomerUpdate


class CustomerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payload: CustomerCreate) -> Customer:
        customer = Customer(**payload.model_dump())
        self.session.add(customer)
        await self.session.flush()
        await self.session.refresh(customer)
        return customer

    async def get_by_id(self, customer_id: UUID) -> Customer | None:
        return await self.session.get(Customer, customer_id)

    async def list(self, *, limit: int = 100, offset: int = 0) -> list[Customer]:
        stmt: Select[tuple[Customer]] = (
            select(Customer)
            .order_by(Customer.created_at.desc(), Customer.id.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, customer: Customer, payload: CustomerUpdate) -> Customer:
        for field_name, value in payload.model_dump(exclude_unset=True).items():
            setattr(customer, field_name, value)

        await self.session.flush()
        await self.session.refresh(customer)
        return customer

    async def delete(self, customer: Customer) -> None:
        await self.session.delete(customer)
        await self.session.flush()
