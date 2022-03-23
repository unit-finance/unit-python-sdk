from distutils.core import setup
setup(
    name='unit-python-sdk',
    packages=['unit', 'unit.api', 'unit.models', 'unit.utils'],
    version='0.10.3',
    license='Mozilla Public License 2.0',
    description='This library provides a python wrapper to http://unit.co API. See https://docs.unit.co/',
    author='unit.co',
    author_email='dev@unit.co',
    url='https://github.com/unit-finance/unit-python-sdk',
    download_url='https://github.com/unit-finance/unit-python-sdk.git',
    keywords=['unit', 'finance', 'banking',
              'banking-as-a-service', 'API', 'SDK'],
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
