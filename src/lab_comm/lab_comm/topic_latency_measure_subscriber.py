
import time
import statistics
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class TopicLatencyMeasureSubscriber(Node):
    def __init__(self):
        super().__init__('topic_latency_measure_subscriber')

        qos = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE
        )

        self.subscription = self.create_subscription(
            String,
            '/topic_latency',
            self.callback,
            qos
        )

        self.latencies = []
        self.last_report = time.monotonic()

        self.get_logger().info('Subscriber pengukur latensi aktif')

    def callback(self, msg):
        received_ns = time.perf_counter_ns()

        try:
            sequence, sent_ns = msg.data.split(',')
            latency_ms = (
                received_ns - int(sent_ns)
            ) / 1_000_000

            self.latencies.append(latency_ms)

        except (ValueError, TypeError):
            self.get_logger().warning('Pesan tidak valid')

    def print_results(self):
        print('\n===== HASIL LATENSI TOPIC 10 Hz =====')
        print(f'Pesan diterima: {len(self.latencies)}')

        if self.latencies:
            print(
                f'Latensi rata-rata: '
                f'{statistics.mean(self.latencies):.3f} ms'
            )
            print(
                f'Latensi minimum : {min(self.latencies):.3f} ms'
            )
            print(
                f'Latensi maksimum : {max(self.latencies):.3f} ms'
            )


def main(args=None):
    rclpy.init(args=args)
    node = TopicLatencyMeasureSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.print_results()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
