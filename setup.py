# Convert our module into a package by adding an empty __init__.py file (not required in Python 3.3+, but good practice)
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ai_travel_itinerary_planner",
    version="2.0",
    author="Sambit",
    packages=find_packages(),
    install_requires=requirements,
)