#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from moveit_msgs.msg import DisplayTrajectory
import serial
import math


# === SLIDER CALIBRATION ===
SLIDER_MAX_M = 0.183     # meters
SLIDER_MAX_STEPS = 2700 # driver units


class UARTFinal(Node):
    def __init__(self):
        super().__init__('uart_final')

        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)
        if self.ser.is_open:
            self.get_logger().info("UART connected")

        self.create_subscription(
            DisplayTrajectory,
            '/display_planned_path',
            self.cb,
            10
        )

    def meters_to_steps(self, pos_m):
        # Clamp to joint limits
        pos_m = max(0.0, min(SLIDER_MAX_M, pos_m))

        steps = (pos_m / SLIDER_MAX_M) * SLIDER_MAX_STEPS
        return int(round(steps))

    def cb(self, msg):
        traj = msg.trajectory[0].joint_trajectory
        joints = traj.joint_names
        final = traj.points[-1].positions

        out = []

        for i, val in enumerate(final):

            # FIRST joint → meters → steps
            if i == 0:
                converted = self.meters_to_steps(val)

            # Other joints → radians → degrees
            else:
                converted = int(round(math.degrees(val)))

            # LAST joint → divide by 2 (your original logic)
            if i == len(final) - 1:
                converted = int(converted / 2)

            out.append(str(converted))

        payload = ",".join(out) + "\n"
        self.ser.write(payload.encode())

        self.get_logger().info(
            f"UART SENT → {payload.strip()} "
        )


def main():
    rclpy.init()
    node = UARTFinal()
    rclpy.spin(node)


if __name__ == '__main__':
    main()

