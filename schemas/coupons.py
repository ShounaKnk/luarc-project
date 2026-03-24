from pydantic import BaseModel

class CreateCoupon(BaseModel):
    coupon_code: str
    total_quantity: int
    
class CouponResponse(BaseModel):
    id: int
    coupon_code: str