from setuptools import setup, find_packages

setup(
    name="earthstar",
    version="0.0.1",
    url='http://github.com/hodgestar/yikes-moles',
    license='MIT',
    description="Earthstar control software and simulator.",
    long_description=open('README.rst', 'r').read(),
    author='Simon Cross',
    author_email='hodgestar+earthstar@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'zmq',
    ],
    entry_points={  # Optional
        'console_scripts': [
            'earthstar-api=earthstar.api:main',
            'earthstar-effectbox=earthstar.effectbox:main',
            'earthstar-simulator=earthstar.simulator:main',
        ],
    },
    scripts=[
        'bin/earthstar-runner',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Games/Entertainment',
    ],
)
