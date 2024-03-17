from setuptools import setup, find_packages

setup(
    name='wtech',
    version='1.2',
    description='That a wtech py-package.',
    author='Wangtry',
    author_email='wangtry3417@gmail.com',
    packages=find_packages(),
    license='MLT',
    license_files=('LICENSE'),
    install_requires=[
        'cryptography',
        'flask',
        'requests',
        'random2',
        'discord'
    ],
)
