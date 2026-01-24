from typing import List, Optional
import uvicorn
from pyguizer import PyGUIzer
from pyguizer.api.app import create_app

@PyGUIzer()
def greet(name: str, age: int, hobbies: List[str] = None, is_active: bool = True) -> str:
    """Generate a personalized greeting message."""
    hobbies_str = f" and enjoy {', '.join(hobbies)}" if hobbies else ""
    status_str = "active" if is_active else "inactive"
    return f"Hello {name}! You are {age} years old, {status_str}{hobbies_str}."

@PyGUIzer()
def calculate_discount(price: float, discount_percentage: float, is_vip: bool = False) -> float:
    """Calculate the final price after applying discounts."""
    base_discount = price * (discount_percentage / 100)
    vip_bonus = price * 0.05 if is_vip else 0
    total_discount = base_discount + vip_bonus
    final_price = price - total_discount
    return round(final_price, 2)

# Run the application if this file is executed directly
if __name__ == "__main__":
    print("🚀 Starting PyGUIzer application...")
    print("📖 Using function: greet")
    
    # Create the FastAPI app using the greet function
    app = create_app(greet)
    
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)

