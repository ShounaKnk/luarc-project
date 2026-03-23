from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    claims = relationship("Claim", back_populates="user")
    
class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True, index=True)
    coupon_code = Column(String, index=True)
    total_quantity = Column(Integer)
    claimed_quantity = Column(Integer, default=0)
    claims = relationship("Claim", back_populates="coupon")
    
class Claim(Base):
    __tablename__ = "claims"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    coupon_id = Column(Integer, ForeignKey("coupons.id"))
    
    user = relationship("User", back_populates="claims")
    coupon = relationship("Coupon", back_populates="claims")