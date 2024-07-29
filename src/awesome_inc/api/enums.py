from enum import Enum
from .models import Country, Customer, Installation, Product, ProductCategory


class ORMTables(Enum):
    country = Country
    customer = Customer
    installation = Installation
    product = Product
    product_category = ProductCategory
