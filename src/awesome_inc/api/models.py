from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List
from datetime import date


class Base(DeclarativeBase):
    pass


class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    region: Mapped[str]

    customers: Mapped[List["Customer"]] = relationship(
        back_populates="country"
    )


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    premium_customer: Mapped[str]

    country: Mapped["Country"] = relationship(back_populates="customers")
    installations: Mapped[List["Installation"]] = relationship(
        back_populates="customer"
    )


class Installation(Base):
    __tablename__ = "installation"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    installation_date: Mapped[date]

    product: Mapped["Product"] = relationship(back_populates="installations")
    customer: Mapped["Customer"] = relationship(back_populates="installations")


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    reference: Mapped[str]
    name: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("product_category.id"))
    price: Mapped[str]

    installations: Mapped[List["Installation"]] = relationship(
        back_populates="product"
    )
    product_category: Mapped["ProductCategory"] = relationship(
        back_populates="products"
    )


class ProductCategory(Base):
    __tablename__ = "product_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    products: Mapped[List["Product"]] = relationship(
        back_populates="product_category"
    )
