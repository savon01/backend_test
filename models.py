from pydantic import BaseModel


class Query(BaseModel):
    cadastre_number: str
    latitude: float
    longitude: float


class QueryHistory(BaseModel):
    id: int
    cadastre_number: str
    latitude: float
    longitude: float
    result: bool
