
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from example_interfaces.action import Fibonacci


class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self.client = ActionClient(
            self, Fibonacci, 'fibonacci'
        )
        self.start_time = 0

    def send_goal(self):
        self.get_logger().info('Menunggu action server...')
        self.client.wait_for_server()

        goal = Fibonacci.Goal()
        goal.order = 10

        self.start_time = time.perf_counter()
        self.get_logger().info('Mengirim goal Fibonacci')

        future = self.client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )
        future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback.sequence
        self.get_logger().info(
            f'Feedback diterima: {feedback}'
        )

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal ditolak')
            return

        self.get_logger().info('Goal diterima server')

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        elapsed = (
            time.perf_counter() - self.start_time
        ) * 1000

        result = future.result().result
        self.get_logger().info(
            f'Hasil: {result.sequence}'
        )
        self.get_logger().info(
            f'Durasi total goal sampai hasil: {elapsed:.3f} ms'
        )


def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionClient()
    node.send_goal()

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
