"""
Simple Sample App Demonstrating PyGUIzer Multi-Function Support

This app shows how users can create a multi-function application
without writing any FastAPI code directly.
"""

from pyguizer import PyGUIzer

# Create a PyGUIzer instance
pyguizer = PyGUIzer()

# Define your functions with the PyGUIzer decorator


@pyguizer
def process_text(text: str, uppercase: bool = False, strip: bool = True) -> str:
    """Process text by applying transformations."""
    if strip:
        text = text.strip()
    if uppercase:
        text = text.upper()
    return text


@pyguizer
def count_words(text: str) -> int:
    """Count the number of words in a text string."""
    if not text:
        return 0
    return len(text.split())


@pyguizer
def get_word_stats(text: str) -> dict:
    """Get detailed word statistics from text."""
    words = text.split()
    word_count = len(words)
    unique_words = len(set(words))
    avg_word_length = (
        sum(len(word) for word in words) / word_count if word_count > 0 else 0
    )

    return {
        "word_count": word_count,
        "unique_words": unique_words,
        "avg_word_length": round(avg_word_length, 2),
        "total_characters": len(text),
    }


@pyguizer
def generate_report(stats: dict, title: str = "Text Analysis Report") -> str:
    """Generate a formatted report from text statistics."""
    return f"""# {title}

Word Count: {stats['word_count']}
Unique Words: {stats['unique_words']}
Average Word Length: {stats['avg_word_length']}
Total Characters: {stats['total_characters']}
"""


if __name__ == "__main__":
    print("=== PyGUIzer Multi-Function App ===")
    print("This app demonstrates how to create a multi-function application")
    print("without writing any FastAPI code.")
    print("\nAvailable functions:")
    for func in pyguizer.registered_functions:
        print(f"  - {func.__name__}: {func.__doc__.splitlines()[0]}")
    print("\nTo run the app, execute:")
    print(
        "python examples/simple_pipeline_app.py  # or: python -m pyguizer run examples/simple_pipeline_app.py"
    )

    # Run the server
    pyguizer.run(title="Simple Multi-Function App", port=8000)
