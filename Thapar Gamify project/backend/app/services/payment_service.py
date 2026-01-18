"""Payment service for handling Razorpay transactions"""
import razorpay
from app.core.config import settings
from sqlalchemy.orm import Session
from app.models import Transaction, User

class PaymentService:
    def __init__(self):
        self.client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

    def create_order(self, user_id: int, amount: float, reward_id: int) -> dict:
        """Create Razorpay order for reward redemption"""
        try:
            order_data = {
                "amount": int(amount * 100),  # Amount in paise
                "currency": "INR",
                "receipt": f"reward_{reward_id}_{user_id}",
                "notes": {
                    "user_id": user_id,
                    "reward_id": reward_id
                }
            }
            
            order = self.client.order.create(data=order_data)
            return order
        except Exception as e:
            return {"error": str(e)}

    def verify_payment(self, payment_id: str, order_id: str, signature: str) -> bool:
        """Verify Razorpay payment signature"""
        try:
            self.client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })
            return True
        except Exception as e:
            return False

    def record_transaction(self, db: Session, user_id: int, transaction_type: str, 
                          amount: int, description: str, related_id: int = None, 
                          related_type: str = None) -> Transaction:
        """Record a transaction"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        balance_before = user.life_points if "points" in transaction_type else user.total_points
        
        if "earned" in transaction_type:
            balance_after = balance_before + amount
        elif "spent" in transaction_type:
            balance_after = balance_before - amount
        else:
            balance_after = balance_before
        
        transaction = Transaction(
            user_id=user_id,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            related_id=related_id,
            related_type=related_type,
            balance_before=balance_before,
            balance_after=balance_after
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        return transaction

    def process_reward_redemption(self, db: Session, user_id: int, reward_id: int, 
                                 points_cost: int, life_points_cost: int) -> dict:
        """Process reward redemption"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"success": False, "error": "User not found"}
        
        if user.total_points < points_cost or user.life_points < life_points_cost:
            return {"success": False, "error": "Insufficient points"}
        
        # Deduct points
        user.total_points -= points_cost
        user.life_points -= life_points_cost
        
        # Record transactions
        self.record_transaction(
            db, user_id, "points_spent",
            points_cost, "Reward redemption", reward_id, "reward"
        )
        
        self.record_transaction(
            db, user_id, "life_points_spent",
            life_points_cost, "Reward redemption", reward_id, "reward"
        )
        
        db.commit()
        
        return {"success": True, "message": "Reward redeemed successfully"}
