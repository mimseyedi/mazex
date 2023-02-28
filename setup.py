import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
install_requires = ['click',]
dependency_links = ['click',]

setup (
 name = 'mazex',
 description = 'mazex is a simple game under the terminal where you have to find the way to the goal in the maze with the most optimal path and solve the challenges.',
 version = '1.0.0',
 packages = find_packages(),
 install_requires = install_requires,
 python_requires='>=3.6',
 entry_points='''
        [console_scripts]
        mazex=mazex.mazex:main
    ''',
 author="mimseyedi",
 keyword="game, maze, terminal, command_line, python",
 long_description=README,
 long_description_content_type="text/markdown",
 license='MIT',
 url='https://github.com/mimseyedi/mazex',
 dependency_links=dependency_links,
 author_email='mim.seyedi@gmail.com',
 classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
    ]
)