import sys
sys.path.append('pycdr-0.1.5')

import pprint
from zenoh import config, Value, Sample, Reliability
import time
import argparse
import json
import zenoh
from pycdr.types import int8, int32, uint32, float32, float64
from pycdr import cdr



conf = zenoh.Config()
zenoh.init_logger()
print("Opening session...")
# conf.insert_json5(zenoh.config.CONNECT_KEY,
#                   json.dumps(["tcp/192.168.1.103:7447"]))
session = zenoh.open(conf)
key = 'rt/api/autoware/get/velocity_limit'

# print(f"Declaring Publisher on '{key}'...")
# pub = session.declare_publisher(key)

@cdr
class Time:
   sec: int32
   nanosec: uint32

@cdr
class VelocityLimitConstraints:
    min_acceleration: float32
    max_jerk: float32
    min_jerk: float32

@cdr
class VelocityLimit:
    stamp: Time
    max_velocity: float32
    use_constraints: bool
    constraints: VelocityLimitConstraints
    sender: str


# builtin_interfaces/Time stamp
#         int32 sec
#         uint32 nanosec
# float32 max_velocity

# bool use_constraints false
# tier4_planning_msgs/VelocityLimitConstraints constraints
#         float32 min_acceleration
#         float32 max_jerk
#         float32 min_jerk

# string sender



def listener(sample: Sample):
    velocity_limit = VelocityLimit.deserialize(sample.payload)
    pprint.pprint(velocity_limit)
    # print(f">> [Subscriber] Received {sample.kind} ('{sample.key_expr}': \n'{sample.payload}')")


print("Declaring Subscriber on '{}'...".format(key))
sub = session.declare_subscriber(key, listener, reliability=Reliability.RELIABLE())


print("Enter 'q' to quit...")
c = '\0'
while c != 'q':
    c = sys.stdin.read(1)
    if c == '':
        time.sleep(1)

# @cdr
# class Vector3:
#     x: float64
#     y: float64
#     z: float64


# @cdr
# class Twist:
#     linear: Vector3
#     angular: Vector3


# idx = 0
# while True:
#     time.sleep(1)
#     # buf = f"[{idx:4d}] {value}"
#     # print(f"Putting Data ('{key}': '{buf}')...")
#     # buf = Twist(linear=Vector3(x=0.0, y=0.0, z=0.0),
#     #             angular=Vector3(x=2.0, y=0.0, z=0.0))
#     linear = Vector3(x=2.0, y=0.0, z=0.0)
#     angular = Vector3(x=0.0, y=0.0, z=0.0)
#     msg = Twist(linear, angular).serialize()
#     # data = Encoder().encode(msg)
#     # data = "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
#     pub.put(msg)
#     # pub.put('Hi')
#     idx += 1

# pub.undeclare()
# session.close()

sub.undeclare()
session.close()