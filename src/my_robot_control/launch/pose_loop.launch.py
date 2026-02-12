from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch

def generate_launch_description():

    moveit_config = (
        MoveItConfigsBuilder(
            robot_name="my_robot",
            package_name="moveit_config"
        )
        .to_moveit_configs()
    )

    demo_launch = generate_demo_launch(moveit_config)

    pose_node = Node(
        package="my_robot_control",
        executable="pose_sequence_loop",
        output="screen",
        parameters=[
            moveit_config.to_dict()   # 🔥 THIS IS THE KEY
        ],
    )

    return LaunchDescription(
        demo_launch.entities + [pose_node]
    )
