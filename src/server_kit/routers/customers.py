from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from server_kit.db import get_db_session
from server_kit.repositories import CustomerRepository
from server_kit.schemas import (
    CustomerCreate,
    CustomerListResponse,
    CustomerRead,
    CustomerUpdate,
)

router = APIRouter(prefix="/api/v1/customers", tags=["customers"])

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


def get_customer_repository(session: DbSession) -> CustomerRepository:
    return CustomerRepository(session)


CustomerRepo = Annotated[CustomerRepository, Depends(get_customer_repository)]


@router.post("", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
async def create_customer(
    payload: CustomerCreate,
    response: Response,
    repository: CustomerRepo,
) -> CustomerRead:
    customer = await repository.create(payload)
    response.headers["Location"] = f"/api/v1/customers/{customer.id}"
    return CustomerRead.model_validate(customer)


@router.get("", response_model=CustomerListResponse)
async def list_customers(
    repository: CustomerRepo,
    limit: int = 100,
    offset: int = 0,
) -> CustomerListResponse:
    customers = await repository.list(limit=limit, offset=offset)
    return CustomerListResponse(
        data=[CustomerRead.model_validate(customer) for customer in customers]
    )


@router.get("/{customer_id}", response_model=CustomerRead)
async def get_customer(
    customer_id: UUID,
    repository: CustomerRepo,
) -> CustomerRead:
    customer = await repository.get_by_id(customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return CustomerRead.model_validate(customer)


@router.patch("/{customer_id}", response_model=CustomerRead)
async def update_customer(
    customer_id: UUID,
    payload: CustomerUpdate,
    repository: CustomerRepo,
) -> CustomerRead:
    customer = await repository.get_by_id(customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    updated_customer = await repository.update(customer, payload)
    return CustomerRead.model_validate(updated_customer)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: UUID,
    repository: CustomerRepo,
) -> Response:
    customer = await repository.get_by_id(customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )

    await repository.delete(customer)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
