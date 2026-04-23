#!/usr/bin/env python3
"""
Wall-following maze navigator for TurtleBot3 — ROS2 Jazzy
Algorithm: right-hand rule (always keep a wall to the right)
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped   # ✅ UPDATED
import math


class MazeNavigator(Node):
    def __init__(self):
        super().__init__('maze_navigator')

        self.scan_sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10)

        # ✅ UPDATED publisher
        self.cmd_pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)

        # Tunable parameters
        self.front_clear   = 0.50
        self.right_target  = 0.35
        self.linear_speed  = 0.15
        self.angular_speed = 0.60

        self.get_logger().info('Maze navigator node started (Jazzy)')

    def get_min(self, ranges, start, end):
        """Minimum valid range in a degree window."""
        sector = [r for r in ranges[start:end]
                  if not math.isnan(r) and not math.isinf(r) and r > 0.05]
        return min(sector) if sector else float('inf')

    def scan_callback(self, msg):
        ranges = msg.ranges

        front = min(
            self.get_min(ranges, 355, 360),
            self.get_min(ranges, 0, 5)
        )
        front_right = self.get_min(ranges, 315, 350)
        right = self.get_min(ranges, 260, 300)

        # ✅ UPDATED command type
        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()

        # ── State machine ─────────────────────────────
        if front < self.front_clear:
            cmd.twist.linear.x  = 0.0
            cmd.twist.angular.z = self.angular_speed
            self.get_logger().info(f'TURN LEFT  | front={front:.2f}m')

        elif right > self.right_target * 2.0:
            cmd.twist.linear.x  = self.linear_speed * 0.5
            cmd.twist.angular.z = -self.angular_speed * 0.5
            self.get_logger().info(f'FIND WALL  | right={right:.2f}m')

        elif right < self.right_target * 0.6:
            cmd.twist.linear.x  = self.linear_speed
            cmd.twist.angular.z = self.angular_speed * 0.4
            self.get_logger().info(f'STEER LEFT | right={right:.2f}m')

        elif front_right < self.front_clear:
            cmd.twist.linear.x  = self.linear_speed * 0.6
            cmd.twist.angular.z = self.angular_speed * 0.3
            self.get_logger().info(f'CORNER     | front_right={front_right:.2f}m')

        else:
            cmd.twist.linear.x  = self.linear_speed
            cmd.twist.angular.z = 0.0
            self.get_logger().info(f'STRAIGHT   | right={right:.2f}m')

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = MazeNavigator()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        # ✅ Publish stop BEFORE shutdown
        stop = TwistStamped()
        stop.header.stamp = node.get_clock().now().to_msg()
        node.cmd_pub.publish(stop)

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
