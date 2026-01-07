from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from glob import glob
import os


def generate_launch_description():

    # -----------------------------
    # Robot State Publisher
    # -----------------------------
    robot_desc_pkg = get_package_share_directory('my_robot_description')
    urdf_file = os.path.join(
        robot_desc_pkg,
        'urdf',
        'my_robot.urdf.xacro'
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': open(urdf_file).read()
        }]
    )

    # -----------------------------
    # ROS2 Control (Controllers)
    # -----------------------------
    control_pkg = get_package_share_directory('my_robot_control')
    control_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(control_pkg, 'launch', 'ros2_control.launch.py')
        )
    )

    # -----------------------------
    # MoveIt
    # -----------------------------
    moveit_pkg = get_package_share_directory('moveit_config')
    moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(moveit_pkg, 'launch', 'demo.launch.py')
        )
    )

    # -----------------------------
    # UART Node
    # -----------------------------
    uart_node = Node(
        package='stm32_bridge',
        executable='uart.py',
        name='moveit_goal_uart',
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        control_launch,
        moveit_launch,
        uart_node
    ])
