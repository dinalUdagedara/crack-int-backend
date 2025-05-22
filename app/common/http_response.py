from typing import Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel

DataT = TypeVar("DataT")


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_pages: int
    total_items: int


class CommonResponse(BaseModel, Generic[DataT]):
    message: str
    success: bool
    payload: Optional[Union[DataT, List[DataT]]]
    meta: Optional[PaginationMeta]
