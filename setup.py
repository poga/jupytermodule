import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jupytermodule",  # Replace with your own username
    version="0.3.0",
    author="Poga",
    author_email="poga.po@gmail.com",
    description="import jupyter notebooks as python modules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/poga/jupytermodule",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
