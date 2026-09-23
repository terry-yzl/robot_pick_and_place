from setuptools import setup


package_name = 'camera_driver'

setup(
    name=package_name,
    version='0.0.1',
    py_modules=['camera_node'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rokae',
    maintainer_email='ros@rokae.com',
    description='ROS2 camera image publisher using OpenCV and cv_bridge',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'camera_node = camera_node:main',
        ],
    },
)