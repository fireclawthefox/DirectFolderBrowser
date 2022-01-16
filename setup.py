import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DirectFolderBrowser",
    version="22.01",
    author="Fireclaw",
    author_email="fireclawthefox@gmail.com",
    description="A simple file and folder browser for Panda3D",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fireclawthefox/DirectFolderBrowser",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Desktop Environment :: File Managers",
    ],
    install_requires=[
        'panda3d',
    ],
    python_requires='>=3.6',
)
