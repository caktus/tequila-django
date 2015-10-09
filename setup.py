from setuptools import setup


setup(
    name='tequila',
    version='0.0.1',
    packages=['tequila'],
    url='https://github.com/caktus/tequila/',
    license='BSD',
    author='Caktus Consulting Group',
    author_email='info@caktusgroup.com',
    description='',
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'deploy=tequila.deploy:main',
        ],
    },
)
