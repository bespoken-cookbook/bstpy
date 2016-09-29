from distutils.core import setup


setup(
    name='LambdaServer',
    version='0.1',
    packages=['LambdaServer'],
    scripts=['bin/LambdaServer'],
    url='https://github.com/bespoken/PythonLambdaServer',
    license='MIT',
    author='OpenDog',
    author_email='bela@xappmedia.com',
    description='Python http server to expose an AWS lambda',
    install_requires=[
        'simplejson'
      ],

)
