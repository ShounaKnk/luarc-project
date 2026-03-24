from pydantic import BaseModel

class ClaimResponse(BaseModel):
    coupon_id: int
    coupon_code: str