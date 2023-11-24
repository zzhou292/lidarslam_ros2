import os

import launch
import launch_ros.actions

from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, PythonExpression


def generate_launch_description():

    main_param_dir = launch.substitutions.LaunchConfiguration(
        'main_param_dir',
        default=os.path.join(
            get_package_share_directory('lidarslam'),
            'param',
            'lidarslam.yaml'))
    
    # rviz_param_dir = launch.substitutions.LaunchConfiguration(
    #     'rviz_param_dir',
    #     default=os.path.join(
    #         get_package_share_directory('lidarslam'),
    #         'rviz',
    #         'mapping.rviz'))

    cpu_id_param = launch.substitutions.LaunchConfiguration(
        'cpu_id',
        default='0')

    # cpu_id = AddLaunchArgument(ld, "cpu_id", default="0")
    # AddLaunchArgument(ld, "cpu_id", default)
    input_cloud_remapping = [
        ('/input_cloud', PythonExpression(["'/chrono_ros_node/output/lidar/data/pointcloud_' + str(", cpu_id_param, ")"]))
    ]

    
    mapping = launch_ros.actions.Node(
        package='scanmatcher',
        executable='scanmatcher_node',
        parameters=[main_param_dir, {'cpu_id': cpu_id_param}],
        remappings=input_cloud_remapping,
        output='screen'
        )

    tf = launch_ros.actions.Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0','0','0','0','0','0','1','base_link','velodyne']
        )


    graphbasedslam = launch_ros.actions.Node(
        package='graph_based_slam',
        executable='graph_based_slam_node',
        parameters=[main_param_dir],
        output='screen'
        )
    
    # rviz = launch_ros.actions.Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     arguments=['-d', rviz_param_dir]
    #     )


    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            'main_param_dir',
            default_value=main_param_dir,
            description='Full path to main parameter file to load'),
        launch.actions.DeclareLaunchArgument(
            'cpu_id',
            default_value=cpu_id_param,
            description='CPU ID for setting dynamic topic name'),
        mapping,
        tf,
        graphbasedslam,
        # rviz,
            ])
