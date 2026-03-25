from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.models import Coupon, Claim
from schemas.coupons import CreateCoupon

class CouponService:
    def __init__(self, db: Session):
        self.db = db
        
    def create_coupon(self, data: CreateCoupon):
        coupon = Coupon(
            coupon_code = data.coupon_code,
            total_quantity = data.total_quantity,
            claimed_quantity = 0
        )
        self.db.add(coupon)
        self.db.commit()
        self.db.refresh(coupon)
        return coupon
    
    def get_coupons(self):
        coupons = self.db.query(Coupon).all()
        results = []        
        for coupon in coupons:
            remaining = coupon.total_quantity - coupon.claimed_quantity
            results.append({
                "id": coupon.id,
                "coupon_code": coupon.coupon_code,
                "remaining_quantity": remaining
            })
        return results
    
    def get_available_coupons(self):
        coupons = self.db.query(Coupon).filter(Coupon.claimed_quantity< Coupon.total_quantity).all()
        return coupons
    
    def claim_coupon(self, coupon_id: int, user: Session):
        try:
            coupon = self.db.execute(
                select(Coupon).where(Coupon.id == coupon_id).with_for_update()
            ).scalar_one()
            
            if coupon.claimed_quantity >= coupon.total_quantity:
                raise HTTPException(status_code=400, detail="Coupon Exhausted")
            coupon.claimed_quantity += 1
            
            claim = Claim(user_id = user["user_id"], coupon_id = coupon_id)
            self.db.add(claim)
            
            self.db.commit()
            return {
                "sucess": True,
                "data": {
                    "message": "Coupon claimed successfully"
                },
                "error": None
            }
        except HTTPException:
            self.db.rollback()
            raise
        except SQLAlchemyError:
            self.db.rollback()
            return HTTPException(status_code=500, detail="Database error")
        except:
            self.db.rollback()
            return HTTPException(status_code=500, detail="unknown error")
        
    def get_my_claims(self, user: Session):
        claims = self.db.query(Claim).join(Coupon).filter(Claim.user_id == user["user_id"]).all()
        result = []
        if claims:
            for claim in claims:
                result.append({
                    "coupon_id": claim.coupon.id,
                    "coupon_code": claim.coupon.coupon_code
                })
            return result
        return {"message": "No coupons claimed yet"}
    
    def coupon_stats(self):
        stats = self.db.query(
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