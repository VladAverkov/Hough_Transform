"""conftest."""


def pytest_configure(config):
    """Pytest configure."""
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
