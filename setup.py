'''
The setup.py file is an essential part of packaging and distributing Python projects. It is used by setuptools (or distutils in older Python versions) to define the configuration of your project,such as its metadata,dependencies, and entry points. This file allows you to specify how your project should be built, installed, and distributed. 
'''

from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """
    Reads the requirements from a given file and returns them as a list of strings.
    
    Args:
        file_path (str): The path to the requirements file. 
    """

    requirement_list : List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            # Read lines from the file
            lines = file.readlines()
            # Process each line to remove whitespace and ignore comments
            for line in lines:
                requirement = line.strip()
                ## ignore empty lines and -e .
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found. No dependencies will be installed.")
    
    return requirement_list

print(get_requirements())


setup(
    name='network_security',
    version='0.0.1',
    author='Muhammad Ehtisham Khan',
    author_email='muhammadehtishamk786@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
)