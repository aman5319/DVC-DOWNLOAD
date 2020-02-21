from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name="dvcdownload",

        version="0.1",
        
        description ="A sample dvc project",
        
        long_description=long_description,
        
        long_description_content_type='text/markdown',
        
        url="https://github.com/aman5319/DVC-DOWNLOAD",
        
        author="Aman Pandey",
        
        author_email="amanpandey5319@gmail.com",
        
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Programming Language :: Python :: 3 :: Only"
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8"
        ],
        keywords="dvc",

        python_requires='~=3.5',
        
        py_modules=["download"],
        
        install_requires=[
            "Click",
            "termcolor",
            "dvc[s3]"
        ],
    
        entry_points="""
            [console_scripts]
            dvcdownload=download:cli
        """,

         project_urls={  isssaai
            'Bug Trackers': 'https://github.com/aman5319/DVC-DOWNLOAD/issues',
            'Source': "https://github.com/aman5319/DVC-DOWNLOAD",
            "Documentation" : "https://github.com/aman5319/DVC-DOWNLOAD/blob/master/README.md"

    },
