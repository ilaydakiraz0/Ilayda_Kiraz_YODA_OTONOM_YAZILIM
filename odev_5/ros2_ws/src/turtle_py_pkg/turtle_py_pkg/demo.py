import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

topic1 = '/turtle1/cmd_vel'
rate_msg = 2

def main(args = None):
    rclpy.init(args = args)
    controlVel = Twist()

    controlVel.linear.x = 2.0;
    controlVel.linear.y = 0.0;
    controlVel.linear.z = 0.0;

    controlVel.angular.x = 0.0;
    controlVel.angular.y = 0.0;
    controlVel.angular.z = 0.8;

    TestNode = Node("test_node")
    publisher = TestNode.create_publisher(Twist, topic1, 1)
    rate = TestNode.create_rate(rate_msg)

    while  rclpy.ok():
        print("Sending control message")
        publisher.publish(controlVel)

        rclpy.spin_once(TestNode)
        rate.sleep()

    TestNode.destroy_node()
    rclpy.shutdown()

if __name__ == 'main':
    main()

