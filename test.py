import sys
sys.path.append('pycdr-0.1.5')

from zenoh import config, Value
import time
import argparse
import json
import zenoh
from pycdr.types import int8, int32, uint32, float64
from pycdr import cdr



conf = zenoh.Config()
zenoh.init_logger()
print("Opening session...")
conf.insert_json5(zenoh.config.CONNECT_KEY,
                  json.dumps(["tcp/192.168.1.103:7447"]))
session = zenoh.open(conf)
key = 'rt/turtle1/cmd_vel'
print(f"Declaring Publisher on '{key}'...")
pub = session.declare_publisher(key)


# class Vector3:
#     def __init__(self, x, y, z):
#         self.x = x
#         self.y = y
#         self.z = z


# class Twist:
#     def __init__(self, linear, angular):
#         self.linear = linear
#         self.angular = angular


# class Encoder(json.JSONEncoder):
#     def default(self, o):
#         return o.__dict__

@cdr
class Vector3:
    x: float64
    y: float64
    z: float64


@cdr
class Twist:
    linear: Vector3
    angular: Vector3


idx = 0
while True:
    time.sleep(1)
    # buf = f"[{idx:4d}] {value}"
    # print(f"Putting Data ('{key}': '{buf}')...")
    # buf = Twist(linear=Vector3(x=0.0, y=0.0, z=0.0),
    #             angular=Vector3(x=2.0, y=0.0, z=0.0))
    linear = Vector3(x=2.0, y=0.0, z=0.0)
    angular = Vector3(x=0.0, y=0.0, z=0.0)
    msg = Twist(linear, angular).serialize()
    # data = Encoder().encode(msg)
    # data = "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
    pub.put(msg)
    # pub.put('Hi')
    idx += 1

pub.undeclare()
session.close()
