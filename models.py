from database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Float
from sqlalchemy.orm import relationship


class Dealer(Base):
    __tablename__ = "dealer"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=True)
    dealer_code = Column(String(64), nullable=True, unique=True)

    def __repr__(self):
        return "{}".format(self.name)


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    dealer_id = Column(Integer, ForeignKey("dealer.id"))
    dealer = relationship("Dealer")
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    email = Column(String(128), nullable=False)
    phone = Column(String(20), nullable=True)
    status = Column(Boolean, default=True)

    def __repr__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer")
    street = Column(String(64), nullable=False)
    city = Column(String(64), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(10), nullable=False)
    latitude = Column(Float, nullable=True, default=0.00)
    longitude = Column(Float, nullable=True, default=0.00)
    status = Column(Boolean, default=True)

    def __repr__(self):
        return "{} {} {}, {} {}".format(self.customer, self.street, self.city, self.state, self.zip_code)


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    dealer_id = Column(ForeignKey("dealer.id"), nullable=False)
    dealer = relationship("Dealer")
    address = Column(String(128), nullable=True)
    active = Column(Boolean)

    def __repr__(self):
        return "{}:{}".format(self.dealer, self.address)


class ProductType(Base):
    __tablename__ = "product_type"
    id = Column(Integer, primary_key=True)
    dealer_id = Column(Integer, ForeignKey("dealer.id"))
    dealer = relationship("Dealer")
    name = Column(String(64), nullable=True)
    active = Column(Boolean)

    def __repr__(self):
        return "{}".format(self.name)


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    dealer_id = Column(Integer, ForeignKey("dealer.id"))
    dealer = relationship("Dealer")
    product_type_id = Column(Integer, ForeignKey("product_type.id"), nullable=False)
    product_type = relationship("ProductType")
    name = Column(String(64), nullable=False)
    description = Column(String(1024), nullable=True)
    item_price = Column(Float, nullable=True)
    active = Column(Boolean)
    location = Column(Integer, ForeignKey("location.id"), nullable=True)

    def __repr__(self):
        return "{}:{}".format(self.id, self.name)


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    dealer_id = Column(Integer, ForeignKey("dealer.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    order_number = Column(Integer, nullable=False)
    order_date = Column(DateTime, nullable=False)
    order_status = Column(Boolean)
    customer = relationship("Customer")
    dealer = relationship("Dealer")

    def __repr__(self):
        return "{}".format(self.order_number)


class OrderDetail(Base):
    __tablename__ = "order_detail"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    order_product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    order_product = relationship("Product")
    order_product_quantity = Column(Integer, nullable=False)
    order_product_item_price = Column(Float, nullable=False)
    order_line_item_total = Column(Float, nullable=False)

    def __repr__(self):
        return "{} {} @ {}".format(
            self.order_product, 
            self.order_product_quantity,
            self.order_product_item_price
        )


class OrderShipping(Base):
    __tablename__ = "order_shipping"
    id = Column(Integer, primary_key=True)
    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)
    address = relationship("Address")
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    order = relationship("Order")
    order_detail_id = Column(Integer, ForeignKey("order_detail.id"))
    order_detail = relationship("OrderDetail")
    shipping_date = Column(DateTime, nullable=False)
    shipping_status = Column(Boolean, default=False)
    shipping_tracking_number = Column(String(64), nullable=False, unique=True)
    shipping_carrier = Column(String(64), nullable=False, unique=True)
    shipping_delivered = Column(Boolean, default=False)
    shipping_final_disposition = Column(String(64), nullable=True)

    def __repr__(self):
        return "{}:{}".format(self.order, self.shipping_status)
