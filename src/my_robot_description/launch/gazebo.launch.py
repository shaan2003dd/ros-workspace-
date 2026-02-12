from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    robot_description = Command([
        "xacro ",
        PathJoinSubstitution([
            FindPackageShare("my_robot_description"),
            "urdf",
            "robot.urdf"
        ])
    ])

    return LaunchDescription([

        # Gazebo with explicit world
        ExecuteProcess(
            cmd=[
                "gz", "sim", "-r",
                PathJoinSubstitution([
                    FindPackageShare("my_robot_description"),
                    "worlds",
                    "empty.sdf"
                ])
            ],
            output="screen"
        ),

        # Robot State Publisher
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": robot_description}],
            output="screen"
        ),

        # Spawn robot
        Node(
            package="ros_gz_sim",
            executable="create",
            arguments=[
                "-name", "my_robot",
                "-topic", "robot_description",
                "-z", "0.2"
            ],
            output="screen"
        ),
    ])

