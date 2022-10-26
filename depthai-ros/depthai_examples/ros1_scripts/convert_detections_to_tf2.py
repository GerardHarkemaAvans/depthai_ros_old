#!/usr/bin/env python3
import rospy
from depthai_ros_msgs.msg import SpatialDetectionArray
#import tf2
# because of transformations
import tf

import tf2_ros
import geometry_msgs.msg

label_map = [
    "person",        "bicycle",      "car",           "motorbike",     "aeroplane",   "bus",         "train",       "truck",        "boat",
    "traffic light", "fire hydrant", "stop sign",     "parking meter", "bench",       "bird",        "cat",         "dog",          "horse",
    "sheep",         "cow",          "elephant",      "bear",          "zebra",       "giraffe",     "backpack",    "umbrella",     "handbag",
    "tie",           "suitcase",     "frisbee",       "skis",          "snowboard",   "sports ball", "kite",        "baseball bat", "baseball glove",
    "skateboard",    "surfboard",    "tennis racket", "bottle",        "wine glass",  "cup",         "fork",        "knife",        "spoon",
    "bowl",          "banana",       "apple",         "sandwich",      "orange",      "broccoli",    "carrot",      "hot dog",      "pizza",
    "donut",         "cake",         "chair",         "sofa",          "pottedplant", "bed",         "diningtable", "toilet",       "tvmonitor",
    "laptop",        "mouse",        "remote",        "keyboard",      "cell phone",  "microwave",   "oven",        "toaster",      "sink",
    "refrigerator",  "book",         "clock",         "vase",          "scissors",    "teddy bear",  "hair drier",  "toothbrush"]


class ConvertDetectionToTf2:

    def __init__(self):
        rospy.init_node("my_node")
        rospy.Subscriber("/stereo_inertial_publisher/color/yolov4_Spatial_detections", SpatialDetectionArray, self.detections_callback, queue_size=1)

        rospy.spin()

    def detections_callback(self, spatialMsgArray):

        for spatialMsg in spatialMsgArray.detections:
            rospy.loginfo(f'Product: {label_map[spatialMsg.results[0].id]})#, score: nog niet berekend')#{label_map[spatialMsg.results[0].score]:.3f}
            print(f'Product: {label_map[spatialMsg.results[0].id]})#, score: nog niet berekend')#{label_map[spatialMsg.results[0].score]:.3f}

            broadcaster = tf2_ros.TransformBroadcaster()
            static_transformStamped = geometry_msgs.msg.TransformStamped()

            static_transformStamped.header.stamp = rospy.Time.now()
            static_transformStamped.header.frame_id = "oak_model_origin"
            static_transformStamped.child_frame_id = label_map[spatialMsg.results[0].id]

            static_transformStamped.transform.translation.x = float(spatialMsg.position.x)
            static_transformStamped.transform.translation.y = float(spatialMsg.position.y)
            static_transformStamped.transform.translation.z = float(spatialMsg.position.z)

            quat = tf.transformations.quaternion_from_euler(
                   float(0),float(0),float(0))
            static_transformStamped.transform.rotation.x = quat[0]
            static_transformStamped.transform.rotation.y = quat[1]
            static_transformStamped.transform.rotation.z = quat[2]
            static_transformStamped.transform.rotation.w = quat[3]

            broadcaster.sendTransform(static_transformStamped)



def main(args=None):

    converter = ConvertDetectionToTf2()



if __name__ == '__main__':
    main()
