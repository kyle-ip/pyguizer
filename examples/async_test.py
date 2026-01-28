import asyncio
import time
from typing import List

from pyguizer import PyGUIzer

# Create a PyGUIzer instance
app = PyGUIzer()


# Sync function
@app
def sync_function(x: int, y: int) -> int:
    """Sync function that sleeps to simulate work."""
    time.sleep(1)  # Simulate blocking work
    return x + y


# Async function
@app
async def async_function(x: int, y: int) -> int:
    """Async function that sleeps to simulate work."""
    await asyncio.sleep(1)  # Simulate non-blocking work
    return x * y


# Another async function
@app
async def async_data_processor(data: List[int]) -> dict:
    """Async function that processes a list of data."""
    await asyncio.sleep(0.5)  # Simulate work
    return {
        "sum": sum(data),
        "average": sum(data) / len(data) if data else 0,
        "max": max(data) if data else 0,
        "min": min(data) if data else 0,
    }


if __name__ == "__main__":
    app.run(title="Async Test App", port=8002)
