from setuptools import setup

setup(name='PySigmoid',
      version='0.3',
      description='A Python Library that Implements Posit',
      url='https://github.com/mightymercado/PySigmoid',
      author='Ken Mercado',
      author_email='mightymercado@gmail.com',
      license='MIT',
      packages=['PySigmoid'],
      install_requires=['spfpm'],
      python_requires='>=3',
      zip_safe=False)

setup(name='PySigmoid.Math',
      version='0.3',
      packages=['PySigmoid.Math'],
      zip_safe=False)
      