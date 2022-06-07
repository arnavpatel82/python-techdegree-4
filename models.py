from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///inventory.db', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Product(Base):
    __tablename__ = 'Store Inventory'

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(Integer)

    def __repr__(self):
        return f'Product Name: {self.product_name}, Product Quantity: {self.product_quantity}, Product Price: {self.product_price}, Date Updated: {self.date_updated}'


if __name__ == "__main__":
    Base.metadata.create_all(engine)