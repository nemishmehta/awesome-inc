from pydantic import BaseModel
from datetime import date


class BaseRequest(BaseModel):
    class Config:
        orm_mode = True


class Country(BaseRequest):
    id: int
    name: str
    region: str


class Customer(BaseRequest):
    id: int
    name: str
    email: str
    country_id: int
    premium_customer: str


class Installation(BaseRequest):
    id: int
    name: str
    description: str
    product_id: int
    customer_id: int
    installation_date: date


class Product(BaseRequest):
    id: int
    reference: str
    name: str
    category_id: int
    price: str


class ProductCategory(BaseRequest):
    id: int
    name: str
