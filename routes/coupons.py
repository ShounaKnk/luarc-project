from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from database.deps import get_db
from models.models import Coupon, Claim
from utils.deps import get_current_user
from schemas.coupons import CreateCoupon, CouponResponse
from schemas.claim import ClaimResponse

router = APIRouter(prefix="/coupons", tags=["Coupons"])

@router.post("/create")
def create_coupon(data: CreateCoupon, db: Session = Depends(get_db)):
    coupon = Coupon(
        coupon_code = data.coupon_code,
        total_quantity = data.total_quantity,
        claimed_quantity = 0
    )
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon


@router.get("/", response_model=list[CouponResponse])
def get_coupons(db: Session = Depends(get_db)):
    coupons = db.query(Coupon).all()
    results = []
    
    for coupon in coupons:
        remaining = coupon.total_quantity - coupon.claimed_quantity
        results.append({
            "id": coupon.id,
            "coupon_code": coupon.coupon_code,
            "remaining_quantity": remaining
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
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        return HTTPException(status_code=500, detail="Database error")
    except:
        db.rollback()
        return HTTPException(status_code=500, detail="unknown error")
    
@router.get("/my-claims", response_model=list[ClaimResponse])
def get_my_claims(db: Session = Depends(get_db), user = Depends(get_current_user)):
    claims = db.query(Claim).join(Coupon).filter(Claim.user_id == user["user_id"]).all()
    result = []
    if claims:
        for claim in claims:
            result.append({
                "coupon_id": claim.coupon.id,
                "coupon_code": claim.coupon.coupon_code
            })
        return result
    return {"message": "No coupons claimed yet"}


@router.get("/coupon-stats")
def coupon_stats(db: Session = Depends(get_db)):
    stats = db.query(
        Coupon.id,
        Coupon.coupon_code,
        func.count(Claim.id).label("total_claims")
    ).outerjoin(Claim).group_by(Coupon.id).all()
    
    return [
        {
            "id": stat.id,
            "coupon_code": stat.coupon_code,
            "total_claims": stat.total_claims
        }
        for stat in stats
    ]
