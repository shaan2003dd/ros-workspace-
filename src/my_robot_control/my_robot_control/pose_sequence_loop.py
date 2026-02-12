import rclpy
from rclpy.node import Node
import time
from moveit.planning import MoveItPy
from moveit.core.robot_state import RobotState

class PoseSequenceLoop(Node):

    def __init__(self):
        super().__init__('pose_sequence_loop')

        self.moveit = MoveItPy(node_name='moveit_py')
        self.arm = self.moveit.get_planning_component('arm')

        self.joint_names = [
            'joint1', 'joint2', 'joint3', 'joint4', 'joint5'
        ]

        # 5 poses (radians!)
        self.poses = [
            [0.0, -0.5, 0.3, 0.0, 0.0],
            [0.3, -0.3, 0.4, 0.2, 0.0],
            [-0.3, -0.6, 0.2, -0.2, 0.1],
            [0.5, -0.4, 0.1, 0.3, -0.1],
            [0.0, -0.5, 0.0, 0.0, 0.0],
        ]

    def run(self):
        while rclpy.ok():
            for idx, pose in enumerate(self.poses):
                self.get_logger().info(f'Executing pose {idx + 1}')

                robot_state = RobotState(self.moveit.get_robot_model())
                robot_state.set_joint_group_positions('arm', pose)

                self.arm.set_start_state_to_current_state()
                self.arm.set_goal_state(robot_state=robot_state)

                plan = self.arm.plan()
                if plan:
                    self.arm.execute()
                    time.sleep(2.0)   # ⬅ VERY IMPORTANT
                else:
                    self.get_logger().error('Planning failed')

def main():
    rclpy.init()
    node = PoseSequenceLoop()
    node.run()
    rclpy.shutdown()
