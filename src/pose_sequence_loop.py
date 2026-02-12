#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class PoseSequenceLoop(Node):
    def __init__(self):
        super().__init__("pose_sequence_loop")

        self.publisher = self.create_publisher(
            JointTrajectory,
            "/arm_controller/joint_trajectory",
            10
        )

        self.joint_names = [
            "BASE_Slider-1", "LINK1_Revolute-2", 
            "LINK2_Revolute-3", "LINK3_Revolute-4"
        ]

        self.poses = [
            [0.00,  0.0,  0.0,  0.0],
            [0.10,  0.5, -0.5,  1.0],
            [0.18, -0.5,  0.5,  2.0],
            [0.10,  1.0,  0.0,  3.0],
            [0.00,  0.0,  0.0,  0.0],
        ]
        
        self.current_pose_idx = 0
        
        # Timer set to 2.5s: 0.5s for movement + 2.0s for delay/pause
        self.timer = self.create_timer(2.5, self.publish_next_pose)
        self.get_logger().info("Fast trajectory loop started with delays")

    def publish_next_pose(self):
        msg = JointTrajectory()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.joint_names = self.joint_names

        point = JointTrajectoryPoint()
        point.positions = self.poses[self.current_pose_idx]
        
        # FAST MOVEMENT: Reach target in 0.5 seconds
        point.time_from_start = Duration(sec=0, nanosec=500000000)

        msg.points.append(point)
        self.publisher.publish(msg)
        
        self.get_logger().info(f"Moving to Pose {self.current_pose_idx} quickly...")
        self.current_pose_idx = (self.current_pose_idx + 1) % len(self.poses)

def main():
    rclpy.init()
    node = PoseSequenceLoop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
