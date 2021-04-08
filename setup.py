import setuptools

VERSION = '1.0.2'

setuptools.setup(
    name='Minecraft-Helpers',
    version=VERSION,
    description='Minecraft server application handler with start, stop, restart, status, and more.',
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
    install_requires=[
        'flask',
        'uwsgi',
    ],
)
