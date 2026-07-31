from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    id: int
    name: str
    description: str
    price: float
    quantity: int
