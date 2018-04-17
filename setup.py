from distutils.core import setup

DISTUTILS_DEBUG = 1

setup(name='BlenderTextGenerator',
      version='0.1',
      description='A pyGTK based application for making 3D text models',
      author='Marko Vejnovic',
      author_email='marko.vejnovic@hotmail.com',
      url='https://gitlab.com/mint-2017/MINT_2017',
      scripts=['BlenderTextGenerator.py', 'BlenderSup.py'])
