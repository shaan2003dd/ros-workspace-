#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from moveit_msgs.msg import DisplayTrajectory
import serial
import math


class UARTFinal(Node):
    def __init__(self):
        super().__init__('uart_final')

        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
        if self.ser.is_open:
            self.get_logger().info("UART connected")

        self.create_subscription(
            DisplayTrajectory,
            '/display_planned_path',
            self.cb,
            10
        )

    def cb(self, msg):
        traj = msg.trajectory[0].joint_trajectory
        joints = traj.joint_names
        final = traj.points[-1].positions

        out = []
        for i, val in enumerate(final):
            name = joints[i]

            # Prismatic joint: meters → mm
            if "Slider" in name or "Prismatic" in name:
                converted = int(val * 1000)
            else:
                # Revolute joint: radians → degrees
                converted = int(round(math.degrees(val)))

            # LAST joint → divide by 2
            if i == len(final) - 1:
                converted = int(converted / 2)

            out.append(converted)

        payload = ",".join(map(str, out)) + "\n"
        self.ser.write(payload.encode())
        self.get_logger().info(f"UART SENT → {payload.strip()}")


def main():
    rclpy.init()
    node = UARTFinal()
    rclpy.spin(node)


if __name__ == '__main__':
    main()

