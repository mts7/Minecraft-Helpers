import setuptools

VERSION = '1.0.3'

setuptools.setup(
    name='Minecraft-Helpers',
    version=VERSION,
    description='Minecraft server application handler with start, stop, '
                'restart, status, and more.',
    url='https://github.com/mts7/Minecraft-Helpers',
    author='Mike Rodarte',
    license='MIT License',
    packages=setuptools.find_packages(exclude=['*_test.', 'test_*.']),
    classifiers=[
        'License:: OSI Approved:: MIT License',
        'Operating System:: OS Independent',
        'Programming Language:: Python:: 3',
        'Programming Language:: Python:: 3.7',
        'Programming Language:: Python:: 3.8',
        'Programming Language:: Python:: 3.9',
    ],
    python_requires='>=3.7',
    dependency_links=[
        'git+https://github.com/mts7/mts-logger@v0.2.4#egg=mts-logger',
    ],
    install_requires=[
        'flask',
        'python-dotenv',
        'uwsgi',
        'pytest',
        'pytest-mock',
    ],
)
