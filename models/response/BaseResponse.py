from dataclasses import dataclass
from typing import Any, Union


@dataclass
class BaseResponse:
    data: Any
    code: int = 500
    message: Union[str, None] = None


