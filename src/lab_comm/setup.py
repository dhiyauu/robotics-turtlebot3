from glob import glob
from setuptools import os, find_packages, setup

package_name = 'lab_comm'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
        'share/ament_index/resource_index/packages',
        ['resource/lab_comm']
    ),
    ('share/lab_comm', ['package.xml']),
    (
        os.path.join('share', 'lab_comm', 'launch'),
        glob('launch/*.launch.py')
    ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dev',
    maintainer_email='dev@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
		'sensor_publisher = lab_comm.sensor_publisher:main',
		'processing_node = lab_comm.processing_node:main',
		'reset_service = lab_comm.reset_service:main',
		'motion_action_server = lab_comm.motion_action_server:main',
		'qos_test_subscriber = lab_comm.qos_test_subscriber:main',
		'topic_latency_subscriber = lab_comm.topic_latency_subscriber:main',
		'reset_system_server = lab_comm.reset_system_server:main',
		'topic_latency_publisher = lab_comm.topic_latency_publisher:main',
		'topic_latency_measure_subscriber = lab_comm.topic_latency_measure_subscriber:main',
		'fibonacci_action_server = lab_comm.fibonacci_action_server:main',
		'fibonacci_action_client = lab_comm.fibonacci_action_client:main',
		'fibonacci_action_cancel_client = lab_comm.fibonacci_action_cancel_client:main',
        ],
    },
)
