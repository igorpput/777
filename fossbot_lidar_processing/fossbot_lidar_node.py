import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String, Bool


class FossbotLidarNode(Node):
    def __init__(self):
        super().__init__('fossbot_lidar_node')

        # Declare configurable parameters
        self.declare_parameter('lidar_topic', '/scan')
        self.declare_parameter('lidar_status_topic', '/lidar_status')
        self.declare_parameter('obstacle_warning_topic', '/obstacle_warning')
        self.declare_parameter('distance_threshold', 1.0)

        lidar_topic = self.get_parameter('lidar_topic').get_parameter_value().string_value
        lidar_status_topic = self.get_parameter('lidar_status_topic').get_parameter_value().string_value
        obstacle_warning_topic = self.get_parameter('obstacle_warning_topic').get_parameter_value().string_value
        self.distance_threshold = self.get_parameter('distance_threshold').get_parameter_value().double_value

        # Subscriber to LIDAR scan data
        self.subscriber = self.create_subscription(
            LaserScan,
            lidar_topic,
            self.scan_callback,
            10
        )

        # Publishers for status text and boolean obstacle warning
        self.status_publisher = self.create_publisher(String, lidar_status_topic, 10)
        self.warning_publisher = self.create_publisher(Bool, obstacle_warning_topic, 10)

        self.get_logger().info(
            f'Node started | Subscribing: {lidar_topic} | '
            f'Status: {lidar_status_topic} | Warning: {obstacle_warning_topic} '
            f'(threshold: {self.distance_threshold} m)'
        )

    def scan_callback(self, msg: LaserScan):
        min_distance = float('inf')
        min_index = -1

        for idx, distance in enumerate(msg.ranges):
            if math.isfinite(distance) and msg.range_min <= distance <= msg.range_max:
                if distance < min_distance:
                    min_distance = distance
                    min_index = idx

        status_msg = String()
        warning_msg = Bool()

        if min_index == -1:
            status_msg.data = 'No obstacle detected within LIDAR range.'
            warning_msg.data = False
            self.get_logger().info(status_msg.data)
        else:
            min_angle = msg.angle_min + min_index * msg.angle_increment
            obstacle_close = min_distance < self.distance_threshold
            status_msg.data = (
                f'Obstacle detected | Min distance: {min_distance:.2f} m | '
                f'Angle: {min_angle:.2f} rad'
            )
            warning_msg.data = obstacle_close
            self.get_logger().info(f'{status_msg.data} | Warning: {obstacle_close}')

        self.status_publisher.publish(status_msg)
        self.warning_publisher.publish(warning_msg)


def main(args=None):
    rclpy.init(args=args)
    node = FossbotLidarNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
