import math
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import Float32


class SensorPublisher(Node):
    def __init__(self):
        super().__init__('sensor_publisher')

        self.declare_parameter('rate_hz', 10.0)
        self.declare_parameter('amplitude', 1.0)
        self.declare_parameter('reliability', 'reliable')
        self.declare_parameter('depth', 10)

        rate = float(self.get_parameter('rate_hz').value)
        amplitude = float(self.get_parameter('amplitude').value)
        reliability = self.get_parameter('reliability').value
        depth = int(self.get_parameter('depth').value)

        if rate <= 0:
            raise ValueError('rate_hz must be greater than 0')

        if depth < 1:
            raise ValueError('depth must be at least 1')

        if reliability == 'reliable':
            rel = ReliabilityPolicy.RELIABLE
        elif reliability == 'best_effort':
            rel = ReliabilityPolicy.BEST_EFFORT
        else:
            raise ValueError(
                "reliability must be 'reliable' or 'best_effort'"
            )

        qos = QoSProfile(
            depth=depth,
            reliability=rel,
            history=HistoryPolicy.KEEP_LAST
        )

        self.pub = self.create_publisher(
            Float32,
            'sensor_data',
            qos
        )

        self.k = 0
        self.sent_count = 0

        self.timer = self.create_timer(
            1.0 / rate,
            self.on_timer
        )

        self.get_logger().info(
            f'Publishing at {rate} Hz, '
            f'QoS={rel.name}, depth={depth}'
        )

    def on_timer(self):
        amplitude = float(
            self.get_parameter('amplitude').value
        )

        msg = Float32()
        msg.data = float(
            amplitude * math.sin(2 * math.pi * self.k / 50.0)
        )

        self.pub.publish(msg)
        self.sent_count += 1
        self.k += 1



def main(args=None):
    rclpy.init(args=args)
    node = SensorPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.get_logger().info(
                f'Total pesan dikirim: {node.sent_count}'
            )
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()

