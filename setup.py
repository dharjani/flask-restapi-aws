from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')
setup(
  name='webservice',
  version='0.0.1',
  description='Basic REST Web APIs',
  long_description=long_description,  
  author='Deepak Harjani',
  author_email='deepakdharjani@gmail.com',
  license='MIT', 
  packages=find_packages(),
  install_requires=['flask','pytest','bcrypt','flask_sqlalchemy','psycopg2-binary','pymysql'] 
)