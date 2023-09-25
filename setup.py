from setuptools import find_packages, setup
from package import Package
import os
setup(
    name='vinylcli',
    # version=os.environ.get('BUILD_VERSION'),
    version='0.0.1',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    # entry_points={
    #     'console_scripts': [
    #         'vinylcli=src.vinylcli:main'
    #     ]
    # },
    install_requires=[
        'boto3==1.24.47',
        'botocore==1.27.47',
        'charset-normalizer==2.1.0',
        'python-dateutil==2.8.2',
        'requests==2.28.1',
    ],
    scripts=['bin/vinylcli', 'bin/vinylcli.py'],
    url='https://github.comcast.com/EFV-CloudServices/vnyl-dns-cli',
    license="MIT"
    # cmdclass={
    #     "package": Package
    # },
)