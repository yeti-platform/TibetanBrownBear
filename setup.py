from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='yeti',
      version="2.0.0",
      description='Your everyday threat intelligence',
      long_description=readme(),
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'Topic :: Threat Intelligence Platform',
      ],
      keywords='yeti threat intelligence platform',
      url='https://github.com/yeti-platform/TibetanBrownBear',
      author='Yeti core developers',
      license='Apache',
      packages=['yeti'],
      install_requires=[
          'python-arango',
          'marshmallow',
          'flask',
          'flask-classful',
          'webargs',
          'tldextract',
          'pytz',
          'python-dateutil',
          'yara-python',
      ],
      entry_points={
          'console_scripts': ['yeticli=yetictl:main'],
      },
      setup_requires=['pytest-runner'],
      test_suite='pytest',
      tests_require=['pytest', 'pytest-cov'],
      include_package_data=True,
      zip_safe=False)
