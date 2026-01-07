from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_demo_launch

def generate_launch_description():
    # Make sure there is NO comma at the end of the line below
    moveit_config = MoveItConfigsBuilder("my_robot.urdf", package_name="moveit_config").to_moveit_configs()
    
    return generate_demo_launch(moveit_config)
