from pyguizer import PyGUIzer

# Create a PyGUIzer instance
app = PyGUIzer()


@app
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


if __name__ == "__main__":
    app.run()
