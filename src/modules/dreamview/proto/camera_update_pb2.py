# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modules/dreamview/proto/camera_update.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="modules/dreamview/proto/camera_update.proto",
    package="apollo.dreamview",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        '\n+modules/dreamview/proto/camera_update.proto\x12\x10\x61pollo.dreamview"o\n\x0c\x43\x61meraUpdate\x12\x14\n\x0clocalization\x18\x01 \x03(\x01\x12\x1e\n\x16localization2camera_tf\x18\x02 \x03(\x01\x12\r\n\x05image\x18\x03 \x01(\x0c\x12\x1a\n\x12image_aspect_ratio\x18\x04 \x01(\x01'
    ),
)


_CAMERAUPDATE = _descriptor.Descriptor(
    name="CameraUpdate",
    full_name="apollo.dreamview.CameraUpdate",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="localization",
            full_name="apollo.dreamview.CameraUpdate.localization",
            index=0,
            number=1,
            type=1,
            cpp_type=5,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="localization2camera_tf",
            full_name="apollo.dreamview.CameraUpdate.localization2camera_tf",
            index=1,
            number=2,
            type=1,
            cpp_type=5,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="image",
            full_name="apollo.dreamview.CameraUpdate.image",
            index=2,
            number=3,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="image_aspect_ratio",
            full_name="apollo.dreamview.CameraUpdate.image_aspect_ratio",
            index=3,
            number=4,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=False,
            default_value=float(0),
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
    serialized_start=65,
    serialized_end=176,
)

DESCRIPTOR.message_types_by_name["CameraUpdate"] = _CAMERAUPDATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CameraUpdate = _reflection.GeneratedProtocolMessageType(
    "CameraUpdate",
    (_message.Message,),
    dict(
        DESCRIPTOR=_CAMERAUPDATE,
        __module__="modules.dreamview.proto.camera_update_pb2"
        # @@protoc_insertion_point(class_scope:apollo.dreamview.CameraUpdate)
    ),
)
_sym_db.RegisterMessage(CameraUpdate)


# @@protoc_insertion_point(module_scope)