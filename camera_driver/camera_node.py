import cv2
import rclpy
from cv_bridge import CvBridge, CvBridgeError
from datetime import datetime
from pathlib import Path
from rclpy.node import Node
from sensor_msgs.msg import Image


class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')

        self.image_topic = self.declare_parameter(
            'image_topic', '/camera/camera/color/image_raw'
        ).value
        self.publisher = self.create_publisher(Image, '/camera/image_raw', 10)
        self.subscription = self.create_subscription(
            Image, self.image_topic, self.image_callback, 10
        )
        self.bridge = CvBridge()
        self.image_dir = Path.home() / 'camera_images'
        self.image_dir.mkdir(parents=True, exist_ok=True)
        self.frame_count = 0
        self.get_logger().info(
            f'Subscribing to RealSense topic: {self.image_topic}'
        )

    def image_callback(self, image_message):
        try:
            frame = self.bridge.imgmsg_to_cv2(image_message, desired_encoding='bgr8')
        except CvBridgeError as error:
            self.get_logger().error(f'Failed to convert ROS image: {error}')
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        image_path = self.image_dir / f'frame_{self.frame_count:06d}_{timestamp}.jpg'
        if not cv2.imwrite(str(image_path), frame):
            self.get_logger().error(f'Failed to save frame to {image_path}')
        self.frame_count += 1

    def destroy_node(self):
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = CameraNode()
        rclpy.spin(node)
    except (RuntimeError, KeyboardInterrupt) as error:
        if isinstance(error, RuntimeError):
            rclpy.logging.get_logger('camera_node').error(str(error))
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()