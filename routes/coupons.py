from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.deps import get_db
from utils.deps import get_current_user
from schemas.coupons import CreateCoupon, CouponResponse
from schemas.claim import ClaimResponse
from services.coupons_service import CouponService

router = APIRouter(prefix="/coupons", tags=["Coupons"])

@router.post("/create")
def create_coupon(data: CreateCoupon, db: Session = Depends(get_db)):
    return CouponService(db).create_coupon(data)

@router.get("/", response_model=list[CouponResponse])
def get_coupons(db: Session = Depends(get_db)):
    return CouponService(db).get_coupons()

@router.get("/available")
def get_available_coupons(db: Session = Depends(get_db)):
    return CouponService(db).get_available_coupons()

@router.post("/claim/{coupon_id}")
def claim_coupon(coupon_id: int, user: Session = Depends(get_current_user),db: Session = Depends(get_db)):
    return CouponService(db).claim_coupon(coupon_id, user)
    
@router.get("/my-claims", response_model=list[ClaimResponse])
def get_my_claims(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return CouponService(db).get_my_claims(user)


@router.get("/coupon-stats")
def coupon_stats(db: Session = Depends(get_db)):
    return CouponService(db).coupon_stats()
