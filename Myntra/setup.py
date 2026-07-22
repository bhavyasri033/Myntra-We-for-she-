from setuptools import setup, find_packages

setup(
    name="ml-intelligence",
    version="1.0.0",
    description="AI Backend Intelligence Service powering Myntra's Regional Fashion Recommendation feature",
    author="Developer 1",
    packages=find_packages(),
    install_requires=[
        "openpyxl>=3.1.0",
        "pandas>=2.0.0",
        "rapidfuzz>=3.0.0",
        "pydantic>=2.0.0",
        "sentence-transformers>=2.2.0",
        "elasticsearch>=8.10.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.20.0",
        "requests>=2.28.0"
    ],
    python_requires=">=3.9",
)
