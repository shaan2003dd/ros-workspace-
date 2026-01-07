#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
import serial
import math


class MoveItCommandUART(Node):
    def __init__(self):
        super().__init__('moveit_command_uart')

        # -------- SERIAL CONFIG --------
        self.ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=115200,
            timeout=0.1
        )

        self.get_logger().info('UART connected')

        # -------- SUBSCRIBE TO MOVEIT COMMAND --------
        self.sub = self.create_subscription(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            self.cb,
            10
        )

        # expected joint order
        self.joint_order = [
            'base_link_Slider',
            'link_1',
            'link_2',
            'link_3'
        ]

    def cb(self, msg: JointTrajectory):
        if not msg.points:
            return

        final_point = msg.points[-1]
        joint_map = dict(zip(msg.joint_names, final_point.positions))

        values = []

        for joint in self.joint_order:
            for name, pos in joint_map.items():
                if joint in name:

                    # prismatic joint
                    if "Slider" in name or "Prismatic" in name:
                        values.append(f"{pos:.3f}")

                    # revolute joint
                    else:
                        deg = (pos * 180.0 / math.pi) % 360.0
                        values.append(f"{deg:.2f}")

                    break

        payload = ",".join(values) + "\n"
        self.ser.write(payload.encode())
        self.get_logger().info(payload.strip())


def main():
    rclpy.init()
    node = MoveItCommandUART()
    rclpy.spin(node)
    node.ser.close()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

