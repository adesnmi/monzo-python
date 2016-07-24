from setuptools import setup

setup(name='mondo-python',
      version='0.1.0',
      description='A python SDK for interacting with the Mondo API.',
      url='https://github.com/muyiwaolu/mondo-python',
      author='Muyiwa Olu-Ogunleye',
      author_email='m.oluogunleye94@gmail.com',
      license='MIT',
      packages=['mondo'],
      install_requires=[
          'requests',
          'python-dotenv'
      ],
      )     
