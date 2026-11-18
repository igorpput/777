import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    lidar_topic = LaunchConfiguration('lidar_topic', default='/scan')
    lidar_status_topic = LaunchConfiguration('lidar_status_topic', default='/lidar_status')
    obstacle_warning_topic = LaunchConfiguration('obstacle_warning_topic', default='/obstacle_warning')
    distance_threshold = LaunchConfiguration('distance_threshold', default='1.0')
    world = LaunchConfiguration('world', default='single_wall.sdf')

    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('fossbot_educational_description'),
                'launch',
                'single.launch.py'
            )
        ),
        launch_arguments={'world': world}.items()
    )

    fossbot_lidar_processing_node = Node(
        package='fossbot_lidar_processing',
        executable='fossbot_lidar_node',
        name='fossbot_lidar_node',
        parameters=[{
            'lidar_topic': lidar_topic,
            'lidar_status_topic': lidar_status_topic,
            'obstacle_warning_topic': obstacle_warning_topic,
            'distance_threshold': ParameterValue(distance_threshold, value_type=float),
        }]
    )

    return LaunchDescription([
        DeclareLaunchArgument('lidar_topic', default_value='/scan'),
        DeclareLaunchArgument('lidar_status_topic', default_value='/lidar_status'),
        DeclareLaunchArgument('obstacle_warning_topic', default_value='/obstacle_warning'),
        DeclareLaunchArgument('distance_threshold', default_value='1.0'),
        DeclareLaunchArgument('world', default_value='single_wall.sdf'),
        sim_launch,
        fossbot_lidar_processing_node,
    ])
