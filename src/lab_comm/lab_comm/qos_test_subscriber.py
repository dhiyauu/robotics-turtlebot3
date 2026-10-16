
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import Float32


class QosTestSubscriber(Node):
    def __init__(self):
        super().__init__('qos_test_subscriber')

        self.declare_parameter('reliability', 'reliable')
        self.declare_parameter('depth', 10)

        reliability = self.get_parameter('reliability').value
        depth = int(self.get_parameter('depth').value)

        if reliability == 'reliable':
            rel = ReliabilityPolicy.RELIABLE
        else:
            rel = ReliabilityPolicy.BEST_EFFORT

        qos = QoSProfile(
            depth=depth,
            reliability=rel,
            history=HistoryPolicy.KEEP_LAST
        )

        self.received_count = 0

        self.sub = self.create_subscription(
            Float32,
            'sensor_data',
            self.on_data,
            qos
        )

        self.get_logger().info(
            f'Subscriber aktif: QoS={reliability}, depth={depth}'
        )

    def on_data(self, msg):
        self.received_count += 1


def main(args=None):
    rclpy.init(args=args)
    node = QosTestSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info(
            f'Total pesan diterima: {node.received_count}'
        )
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
