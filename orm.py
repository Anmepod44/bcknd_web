from typing import Optional

from pydantic import EmailStr

from redis_om import (
    Field,
    HashModel,
    get_redis_connection,
    JsonModel,
    EmbeddedJsonModel,
    Migrator
)

redis = get_redis_connection(host="localhost",port=6379)

class Department(EmbeddedJsonModel):
    serial_no:str
    name:str

    class Meta:
        database = redis

class Features(EmbeddedJsonModel):
    name:str=Field(index=True)
    description:str
    image:str
    cta:str

    class Meta:
        database = redis


class Product(JsonModel):
    name:str=Field(index=True)
    image:str
    description:str
    department:Department
    features:list[Features]

    class Meta:
        database = redis


class Package(JsonModel):
    name:str=Field(index=True)
    image:str
    description:str
    products:list[Product]

    class Meta:
        database = redis