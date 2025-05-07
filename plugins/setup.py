from setuptools import setup

setup(
    name="pytest-suite-timeout",
    version="1.0",
    py_modules=["pytest_suite_timeout"],
    entry_points={"pytest11": ["suite_timeout = pytest_suite_timeout"]},
    description="Pytest plugin to enforce per-suite timeout",
    author="Your Name",
)
