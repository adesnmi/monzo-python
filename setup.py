from setuptools import setup

setup(name='monzo',
      version='0.10.0',
      description='A python SDK for interacting with the Monzo API.',
      url='https://github.com/muyiwaolu/monzo-python',
      author='Muyiwa Olu',
      author_email='muyiolu94@gmail.com',
      license='MIT',
      packages=['monzo'],
      install_requires=[
          'requests==2.20.0',
          'requests-oauthlib==1.0.0',
          'python-dotenv==0.5.1'
      ],
      )
