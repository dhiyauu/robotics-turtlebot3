
import time
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import Float32


class TopicLatencySubscriber(Node):
    def __init__(self):
        super().__init__('topic_latency_subscriber')

        qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST
        )

        self.sub = self.create_subscription(
            Float32,
            'sensor_data',
            self.on_message,
            qos
        )

        self.received_count = 0
        self.latencies = []

        self.get_logger().info('Subscriber aktif')

    def on_message(self, msg):
        self.received_count += 1

        # Placeholder: Float32 tidak menyimpan waktu kirim.
        # Pengukuran latensi akurat membutuhkan timestamp
        # pengiriman yang disertakan pada setiap pesan.
        
    def print_results(self):
        self.get_logger().info(
            f'Total pesan diterima: {self.received_count}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = TopicLatencySubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.print_results()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
