
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class ResetSystemServer(Node):
    def __init__(self):
        super().__init__('reset_system_server')

        self.service = self.create_service(
            Trigger,
            '/reset_system',
            self.reset_callback
        )

        self.get_logger().info(
            'Service /reset_system siap'
        )

    def reset_callback(self, request, response):
        response.success = True
        response.message = 'Reset system berhasil'
        self.get_logger().info('Request reset diterima')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = ResetSystemServer()

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
