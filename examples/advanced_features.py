from datetime import datetime
from typing import List, Optional

from pyguizer import PyGUIzer

# Create a PyGUIzer instance
app = PyGUIzer()


# Example 1: Function with file upload widget
@app
async def process_file(file: str, process_type: str = "analyze") -> str:
    """Process an uploaded file with different processing types.

    Args:
        file: Uploaded file (will be handled as file upload widget)
        process_type: Type of processing to apply

    Returns:
        Processing result message
    """
    return f"Processed file '{file}' with {process_type} processing"


# Example 2: Function with date/time picker widgets
@app
async def schedule_event(title: str, event_date: datetime, event_time: str) -> str:
    """Schedule an event with date and time pickers.

    Args:
        title: Event title
        event_date: Event date (will be handled as date picker)
        event_time: Event time (will be handled as time picker)

    Returns:
        Scheduled event details
    """
    return f"Scheduled event '{title}' for {event_date.strftime('%Y-%m-%d')} at {event_time}"


# Example 3: Function with multiple input types
@app
async def calculate_discount(
    price: float,
    discount_percentage: float,
    is_vip: bool = False,
    promo_code: Optional[str] = None,
) -> float:
    """Calculate discount with different input types.

    Args:
        price: Original price
        discount_percentage: Discount percentage
        is_vip: Whether customer is VIP
        promo_code: Optional promo code

    Returns:
        Final price after discount
    """
    discount = price * (discount_percentage / 100)
    if is_vip:
        discount += price * 0.05  # Additional 5% discount for VIPs
    if promo_code == "SAVE10":
        discount += price * 0.10  # Additional 10% discount for promo code
    final_price = max(0, price - discount)
    return round(final_price, 2)


# Example 4: Function that returns data suitable for chart visualization
@app
async def generate_sales_data(months: int = 12) -> List[float]:
    """Generate sample sales data for visualization.

    Args:
        months: Number of months to generate data for

    Returns:
        List of sales values (will be visualized as chart)
    """
    import random

    return [random.uniform(1000, 5000) for _ in range(months)]


# Example 5: Function with nested categories (using function groups)
@app
async def analyze_sales_data(
    sales_data: List[float],
    analysis_type: str = "trend",
    include_forecast: bool = False,
) -> dict:
    """Analyze sales data with different analysis types.

    Args:
        sales_data: List of sales values
        analysis_type: Type of analysis to perform
        include_forecast: Whether to include sales forecast

    Returns:
        Analysis results
    """
    if not sales_data:
        return {"error": "No sales data provided"}

    avg_sales = sum(sales_data) / len(sales_data)
    max_sales = max(sales_data)
    min_sales = min(sales_data)

    result = {
        "average_sales": round(avg_sales, 2),
        "max_sales": round(max_sales, 2),
        "min_sales": round(min_sales, 2),
        "total_sales": round(sum(sales_data), 2),
        "analysis_type": analysis_type,
    }

    if include_forecast:
        # Simple forecast: average + 5%
        forecast = avg_sales * 1.05
        result["forecast"] = round(forecast, 2)

    return result


# Example 6: Function that returns structured data for table visualization
@app
async def generate_employee_data(count: int = 5) -> List[dict]:
    """Generate sample employee data for table visualization.

    Args:
        count: Number of employees to generate

    Returns:
        List of employee dictionaries
    """
    import random

    departments = ["Engineering", "Marketing", "Sales", "HR", "Finance"]

    employees = []
    for i in range(count):
        employee = {
            "id": i + 1,
            "name": f"Employee {i + 1}",
            "department": random.choice(departments),
            "salary": round(random.uniform(50000, 150000), 2),
            "hire_date": f"2023-{random.randint(1, 12)}-{random.randint(1, 28)}",
        }
        employees.append(employee)

    return employees


# Example 7: Function with batch processing potential
@app
async def process_numbers(numbers: List[int], operation: str = "sum") -> dict:
    """Process a list of numbers with different operations.

    Args:
        numbers: List of numbers to process
        operation: Operation to perform (sum, average, max, min)

    Returns:
        Processing result
    """
    if not numbers:
        return {"error": "No numbers provided"}

    if operation == "sum":
        result = sum(numbers)
    elif operation == "average":
        result = sum(numbers) / len(numbers)
    elif operation == "max":
        result = max(numbers)
    elif operation == "min":
        result = min(numbers)
    else:
        return {"error": f"Invalid operation: {operation}"}

    return {
        "operation": operation,
        "result": round(result, 2) if isinstance(result, float) else result,
        "count": len(numbers),
    }


# Example 8: Function with color picker
@app
async def design_element(
    element_name: str, background_color: str = "#ffffff", text_color: str = "#000000"
) -> dict:
    """Design an element with color pickers.

    Args:
        element_name: Element name
        background_color: Background color (will be handled as color picker)
        text_color: Text color (will be handled as color picker)

    Returns:
        Design details
    """
    return {
        "element": element_name,
        "background_color": background_color,
        "text_color": text_color,
        "design_ready": True,
    }


# Run the application if this file is executed directly
if __name__ == "__main__":
    app.run(title="Advanced Features Example", port=8001)
