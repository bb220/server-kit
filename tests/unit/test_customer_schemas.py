from datetime import datetime, timezone
from uuid import uuid4

from server_kit.schemas import (
    CustomerCreate,
    CustomerListResponse,
    CustomerRead,
    CustomerUpdate,
)


def test_customer_create_schema_requires_minimal_fields():
    payload = CustomerCreate(name="Jane Doe", city="Boston", state="MA")

    assert payload.name == "Jane Doe"
    assert payload.city == "Boston"
    assert payload.state == "MA"


def test_customer_update_schema_omits_unset_fields():
    payload = CustomerUpdate(city="Providence")

    assert payload.model_dump(exclude_unset=True) == {"city": "Providence"}


def test_customer_read_schema_validates_from_attributes():
    customer = type(
        "CustomerStub",
        (),
        {
            "id": uuid4(),
            "name": "Jane Doe",
            "city": "Boston",
            "state": "MA",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
    )()

    result = CustomerRead.model_validate(customer)

    assert result.name == "Jane Doe"
    assert result.city == "Boston"
    assert result.state == "MA"


def test_customer_list_response_wraps_customer_reads():
    customer = CustomerRead(
        id=uuid4(),
        name="Jane Doe",
        city="Boston",
        state="MA",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    response = CustomerListResponse(data=[customer])

    assert response.model_dump()["data"][0]["name"] == "Jane Doe"
