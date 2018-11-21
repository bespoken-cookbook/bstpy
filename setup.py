from distutils.core import setup


setup(
    name='LambdaServer',
    version='0.3',
    packages=['LambdaServer'],
    scripts=['bin/bstpy'],
    url='https://github.com/bespoken/bstpy',
    license='MIT',
    author='OpenDog',
    author_email='bela@xappmedia.com',
    description='Python http server to expose an AWS lambda',
    install_requires=[
        'json'
      ],

)
