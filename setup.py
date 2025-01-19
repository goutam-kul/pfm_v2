from setuptools import setup, find_packages

def parse_requirements(filename):
    """Load dependencies from a requirements.txt file."""
    with open(filename, "r") as req_file:
        return [line.strip() for line in req_file if line and not line.startswith("#")]

setup(
    name="personal_finance_manager_v2",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
        ]
    },
)