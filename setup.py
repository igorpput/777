from setuptools import find_packages, setup
from glob import glob

package_name = 'fossbot_lidar_processing'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='igorp',
    maintainer_email='igorp@todo.todo',
    description='LIDAR processing node for FOSSBot',
    license='Apache-2.0',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'fossbot_lidar_node = fossbot_lidar_processing.fossbot_lidar_node:main',
        ],
    },
)
