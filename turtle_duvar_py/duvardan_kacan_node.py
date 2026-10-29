import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class DuvardanKacanTurtle(Node):
    def __init__(self):
        super().__init__('duvardan_kacan_node')

        # Parametreler (Bonus kısım)
        self.declare_parameter('forward_speed', 2.0)
        self.declare_parameter('turn_speed', 1.5)
        self.declare_parameter('min_limit', 1.0)
        self.declare_parameter('max_limit', 10.0)

        # /turtle1/cmd_vel yayıncısı
        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # /turtle1/pose abonesi
        self.pose_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        self.current_pose = None

        # Saniyede 1 kez log yazdırma zamanlayıcısı
        self.log_timer = self.create_timer(1.0, self.log_callback)

        # 10 Hz (0.1 sn) kontrol döngüsü
        self.control_timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info('Duvardan Kacan Kaplumbaga dugumu baslatildi.')

    def pose_callback(self, msg: Pose):
        self.current_pose = msg

    def log_callback(self):
        if self.current_pose is not None:
            self.get_logger().info(
                f'Konum -> X: {self.current_pose.x:.2f}, Y: {self.current_pose.y:.2f}'
            )

    def control_loop(self):
        if self.current_pose is None:
            return

        forward_speed = self.get_parameter('forward_speed').value
        turn_speed = self.get_parameter('turn_speed').value
        min_limit = self.get_parameter('min_limit').value
        max_limit = self.get_parameter('max_limit').value

        twist_msg = Twist()

        # x veya y sınır dışına çıkarsa dön
        if (self.current_pose.x < min_limit or self.current_pose.x > max_limit or
                self.current_pose.y < min_limit or self.current_pose.y > max_limit):
            twist_msg.linear.x = 0.5
            twist_msg.angular.z = turn_speed
        else:
            twist_msg.linear.x = forward_speed
            twist_msg.angular.z = 0.0

        self.cmd_vel_pub.publish(twist_msg)


def main(args=None):
    rclpy.init(args=args)
    node = DuvardanKacanTurtle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
