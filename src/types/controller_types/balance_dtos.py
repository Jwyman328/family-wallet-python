from pydantic import BaseModel


class GetBalanceResponseDto(BaseModel):
    total: str
    spendable: str
    confirmed: str
