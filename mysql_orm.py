from sqlalchemy import Column, String, Integer, ForeignKey, Text, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# SQLAlchemy setup for MySQL
engine = create_engine('mysql+pymysql://root:example@localhost:3306/ZAHLENTECH_PRODUCTS')
Session = sessionmaker(bind=engine)
session = Session()

# Association table for many-to-many relationship between Products and Features
product_feature_association = Table(
    'product_feature_association',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('feature_id', Integer, ForeignKey('features.id'))
)

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    serial_no = Column(String(50), unique=True, nullable=False)  # Specified length of 50
    name = Column(String(100), nullable=False)  # Specified length of 100


class Features(Base):
    __tablename__ = 'features'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)  # Specified length of 100
    description = Column(Text)
    image = Column(String(255))  # Specified length of 255
    cta = Column(String(255))  # Specified length of 255
    products = relationship(
        "Product",
        secondary=product_feature_association,
        back_populates="features"
    )


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)  # Specified length of 100
    image = Column(String(255))  # Specified length of 255
    description = Column(Text)
    department_id = Column(Integer, ForeignKey('departments.id'))
    department = relationship("Department")
    features = relationship(
        "Features",
        secondary=product_feature_association,
        back_populates="products"
    )


class Package(Base):
    __tablename__ = 'packages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)  # Specified length of 100
    image = Column(String(255))  # Specified length of 255
    description = Column(Text)
    products = relationship("Product", secondary='package_product_association')


# Association table for many-to-many relationship between Packages and Products
package_product_association = Table(
    'package_product_association',
    Base.metadata,
    Column('package_id', Integer, ForeignKey('packages.id')),
    Column('product_id', Integer, ForeignKey('products.id'))
)


# Creating the tables in the database
Base.metadata.create_all(engine)