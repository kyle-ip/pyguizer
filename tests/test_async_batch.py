import asyncio

import aiohttp
import pytest


def test_async_batch():
    """Test batch processing with async and sync functions."""

    async def run_test():
        url = "http://localhost:8002/api/batch"

        # Create batch request with multiple functions
        batch_data = {
            "functions": [
                {"name": "sync_function", "inputs": {"x": 10, "y": 20}},
                {"name": "async_function", "inputs": {"x": 5, "y": 6}},
                {"name": "sync_function", "inputs": {"x": 100, "y": 200}},
                {"name": "async_function", "inputs": {"x": 10, "y": 10}},
                {"name": "async_data_processor", "inputs": {"data": [1, 2, 3, 4, 5]}},
            ]
        }

        print("Sending batch request...")
        start_time = asyncio.get_event_loop().time()

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=batch_data) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(
                            f"Batch request sent successfully. Batch ID: "
                            f"{result['batch_id']}"
                        )

                        # Wait a bit for processing to complete
                        await asyncio.sleep(3)

                        # Get batch results
                        batch_status_url = (
                            f"http://localhost:8002/api/tasks/{result['batch_id']}"
                        )
                        async with session.get(batch_status_url) as status_response:
                            if status_response.status == 200:
                                batch_status = await status_response.json()
                                event_loop = asyncio.get_event_loop()
                                elapsed_time = event_loop.time() - start_time
                                print("\nBatch processing completed in")
                                print(f"{elapsed_time:.2f} seconds")
                                print(f"Status: {batch_status['status']}")
                                print(f"Progress: {batch_status['progress']}")
                                print(f"Message: {batch_status['message']}")
                                print("\nResults:")
                                for item in batch_status["result"]:
                                    if "error" in item:
                                        print(
                                            f"{item['function']}: ERROR - "
                                            f"{item['error']}"
                                        )
                                    else:
                                        print(f"{item['function']}: {item['result']}")
                            else:
                                print(
                                    f"Failed to get batch status: "
                                    f"{status_response.status}"
                                )
                    else:
                        print(f"Failed to send batch request: {response.status}")
                        print(await response.text())
            except aiohttp.ClientConnectorError:
                pytest.skip(
                    "Skipping test because server is not running on localhost:8002"
                )

    asyncio.run(run_test())


if __name__ == "__main__":
    test_async_batch()
