from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='loadleveler-client',

    version='0.1.0',

    description='Loadleveler Client',
    long_description=long_description,

    url='https://github.com/perillaroc/nwpc-operation-system-tool',

    author='perillaroc',
    author_email='perillaroc@gmail.com',

    license='GPL-3.0',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],

    keywords='nwpc loadleveler client',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    include_package_data=True,
    package_data={
        'loadleveler_client': ['conf/*.config']
    },

    install_requires=[],

    # extras_require={
    #     'test': ['pytest'],
    # },

    entry_points={
        'console_scripts': [
            'llclient=loadleveler_client.llclient:cli'
        ]
    }
)
