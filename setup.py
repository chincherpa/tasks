import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="todos",
    version="0.0.2",
    author="chincherpa",
    author_email="accounts@mail.de",
    description="Python CLI to manage your todos, with comments, tags and colors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chincherpa/todos",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["t=todos.todos:main"]},
    python_requires='>=3.6',
)
