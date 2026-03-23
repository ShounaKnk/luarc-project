from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.deps import get_db
from models.models import Coupon, Claim
from utils.deps import get_current_user

router = APIRouter(prefix="/coupons", tags=["Coupons"])

@router.post("/create")
def create_coupon(code: str, total_quantity: int, db: Session = Depends(get_db)):
    coupon = Coupon(
        coupon_code = code,
        total_quantity = total_quantity,
        claimed_quantity = 0
    )
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon


@router.get("/")
def get_coupons(db: Session = Depends(get_db)):
    coupons = db.query(Coupon).all()
    results = []
    
    for coupon in coupons:
        remaining = coupon.total_quantity - coupon.claimed_quantity
        results.append({
            "id": coupon.id,
            "coupon_code": coupon.coupon_code,
            "remaining": remaining
        })
    return results

@router.get("/available")
def get_available_coupons(db: Session = Depends(get_db)):
    coupons = db.query(Coupon).filter(Coupon.claimed_quantity< Coupon.total_quantity).all()
    return coupons

@router.post("/claim/{coupon_id}")
def claim_coupon(
    coupon_id: int,
    db: Session = Depends(get_db),
    user: Session = Depends(get_current_user)
):
    try:
        coupon = db.execute(
            select(Coupon).where(Coupon.id == coupon_id).with_for_update()
        ).scalar_one()
        
        if coupon.claimed_quantity >= coupon.total_quantity:
            raise HTTPException(status_code=400, detail="Coupon Exhausted")
        coupon.claimed_quantity += 1
        
        claim = Claim(user_id = user["user_id"], coupon_id = coupon_id)
        db.add(claim)
        
        db.commit()
        return {"message": "Coupon claimed successfully"}
    except:
        db.rollback()
        raise
    
@router.get("/my-claims")
def get_my_claims(db: Session = Depends(get_db), user = Depends(get_current_user)):
    claims = db.query(Claim).join(Coupon).filter(Claim.user_id == user["user_id"]).all()
    result = []
    for claim in claims:
        result.append({
            "coupon_id": claim.coupon.id,
            "coupon_code": claim.coupon.code
        })
    return result 