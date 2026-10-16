
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TopicLatencyPublisher(Node):
    def __init__(self):
        super().__init__('topic_latency_publisher')

        self.publisher = self.create_publisher(
            String, '/topic_latency', 10
        )

        self.sequence = 0
        self.timer = self.create_timer(0.1, self.publish_message)

        self.get_logger().info('Publisher Topic berjalan pada 10 Hz')

    def publish_message(self):
        msg = String()
        msg.data = f'{self.sequence},{time.perf_counter_ns()}'
        self.publisher.publish(msg)
        self.sequence += 1


def main(args=None):
    rclpy.init(args=args)
    node = TopicLatencyPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
