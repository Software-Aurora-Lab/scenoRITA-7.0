# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modules/perception/lidar/app/proto/lidar_obstacle_tracking_config.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="modules/perception/lidar/app/proto/lidar_obstacle_tracking_config.proto",
    package="apollo.perception.lidar",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        '\nGmodules/perception/lidar/app/proto/lidar_obstacle_tracking_config.proto\x12\x17\x61pollo.perception.lidar"\xab\x01\n\x1bLidarObstacleTrackingConfig\x12\x35\n\x14multi_target_tracker\x18\x01 \x01(\t:\x17\x44ummyMultiTargetTracker\x12)\n\x10\x66rame_classifier\x18\x02 \x01(\t:\x0f\x44ummyClassifier\x12*\n\x11\x66usion_classifier\x18\x03 \x01(\t:\x0f\x44ummyClassifier'
    ),
)


_LIDAROBSTACLETRACKINGCONFIG = _descriptor.Descriptor(
    name="LidarObstacleTrackingConfig",
    full_name="apollo.perception.lidar.LidarObstacleTrackingConfig",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="multi_target_tracker",
            full_name="apollo.perception.lidar.LidarObstacleTrackingConfig.multi_target_tracker",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=True,
            default_value=_b("DummyMultiTargetTracker").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="frame_classifier",
            full_name="apollo.perception.lidar.LidarObstacleTrackingConfig.frame_classifier",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=True,
            default_value=_b("DummyClassifier").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="fusion_classifier",
            full_name="apollo.perception.lidar.LidarObstacleTrackingConfig.fusion_classifier",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=True,
            default_value=_b("DummyClassifier").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=101,
    serialized_end=272,
)

DESCRIPTOR.message_types_by_name[
    "LidarObstacleTrackingConfig"
] = _LIDAROBSTACLETRACKINGCONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LidarObstacleTrackingConfig = _reflection.GeneratedProtocolMessageType(
    "LidarObstacleTrackingConfig",
    (_message.Message,),
    dict(
        DESCRIPTOR=_LIDAROBSTACLETRACKINGCONFIG,
        __module__="modules.perception.lidar.app.proto.lidar_obstacle_tracking_config_pb2"
        # @@protoc_insertion_point(class_scope:apollo.perception.lidar.LidarObstacleTrackingConfig)
    ),
)
_sym_db.RegisterMessage(LidarObstacleTrackingConfig)


# @@protoc_insertion_point(module_scope)