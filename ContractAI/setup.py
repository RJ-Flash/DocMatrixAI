from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="contractai",
    version="0.1.0",
    author="DocMatrix AI Team",
    author_email="info@docmatrix.ai",
    description="AI-powered contract analysis platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/docmatrix/contractai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "contractai=app.main:run_app",
        ],
    },
) 