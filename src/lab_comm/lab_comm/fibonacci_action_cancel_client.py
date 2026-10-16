
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from example_interfaces.action import Fibonacci


class CancelClient(Node):
    def __init__(self):
        super().__init__('fibonacci_cancel_client')
        self.client = ActionClient(
            self, Fibonacci, 'fibonacci'
        )

    def run_test(self):
        self.client.wait_for_server()

        goal = Fibonacci.Goal()
        goal.order = 20

        self.get_logger().info('Mengirim goal order=20')
        future = self.client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )
        future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(
            f"Feedback: {list(feedback_msg.feedback.sequence)}"
        )

    def goal_response_callback(self, future):
        self.goal_handle = future.result()

        if not self.goal_handle.accepted:
            self.get_logger().info('Goal ditolak')
            return

        self.get_logger().info(
            'Goal diterima. Menunggu 1,5 detik sebelum membatalkan.'
        )
        self.cancel_timer = self.create_timer(
            1.5, self.cancel_goal
        )

    def cancel_goal(self):
        self.cancel_timer.cancel()
        self.get_logger().info('Mengirim permintaan pembatalan')

        future = self.goal_handle.cancel_goal_async()
        future.add_done_callback(self.cancel_response_callback)

    def cancel_response_callback(self, future):
        response = future.result()

        if response.goals_canceling:
            self.get_logger().info(
                'Permintaan pembatalan diterima server'
            )
        else:
            self.get_logger().info(
                'Permintaan pembatalan tidak diterima'
            )


def main(args=None):
    rclpy.init(args=args)
    node = CancelClient()

    try:
        node.run_test()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
