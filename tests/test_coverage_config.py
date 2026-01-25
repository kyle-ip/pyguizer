"""Test coverage configuration and utilities."""

import coverage
import pytest


def pytest_configure(config):
    """Configure pytest with coverage settings."""
    # Start coverage
    cov = coverage.Coverage(
        source=["pyguizer"],
        omit=["*/tests/*", "*/test_*.py", "*/__pycache__/*", "*/venv/*", "*/env/*"],
    )
    cov.start()
    config._coverage = cov


def pytest_unconfigure(config):
    """Clean up coverage after tests."""
    if hasattr(config, "_coverage"):
        cov = config._coverage
        cov.stop()
        cov.save()

        # Generate report
        try:
            cov.report()
            # Optionally generate HTML report
            # cov.html_report(directory='htmlcov')
        except Exception as e:
            print(f"Coverage report generation failed: {e}")


@pytest.fixture(scope="session")
def coverage_report():
    """Fixture to generate coverage report."""
    yield
    # Coverage report is generated in pytest_unconfigure
