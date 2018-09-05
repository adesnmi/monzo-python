from setuptools import setup

setup(name='monzo',
      version='0.6.0',
      description='A python SDK for interacting with the Monzo API.',
      url='https://github.com/muyiwaolu/monzo-python',
      author='Muyiwa Olu-Ogunleye',
      author_email='m.oluogunleye94@gmail.com',
      license='MIT',
      packages=['monzo'],
      install_requires=[
          'requests',
          'python-dotenv'
      ],
      )
