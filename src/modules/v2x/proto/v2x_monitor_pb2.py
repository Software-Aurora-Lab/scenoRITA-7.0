# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modules/v2x/proto/v2x_monitor.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import enum_type_wrapper

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="modules/v2x/proto/v2x_monitor.proto",
    package="apollo.v2x",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        '\n#modules/v2x/proto/v2x_monitor.proto\x12\napollo.v2x"Y\n\x08ObuAlarm\x12\x10\n\x08mode_num\x18\x01 \x02(\x01\x12(\n\terror_num\x18\x02 \x02(\x0e\x32\x15.apollo.v2x.ErrorCode\x12\x11\n\terror_msg\x18\x03 \x02(\t*_\n\tErrorCode\x12\t\n\x04LTEV\x10\xf4\x03\x12\x08\n\x03NET\x10\xf5\x03\x12\x08\n\x03\x43PU\x10\xf6\x03\x12\x08\n\x03MEM\x10\xf7\x03\x12\x08\n\x03GPS\x10\xf8\x03\x12\x08\n\x03MAP\x10\xfe\x03\x12\t\n\x04SPAT\x10\xff\x03\x12\n\n\x05OBUID\x10\xe7\x07'
    ),
)

_ERRORCODE = _descriptor.EnumDescriptor(
    name="ErrorCode",
    full_name="apollo.v2x.ErrorCode",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="LTEV", index=0, number=500, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="NET", index=1, number=501, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="CPU", index=2, number=502, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="MEM", index=3, number=503, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="GPS", index=4, number=504, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="MAP", index=5, number=510, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="SPAT", index=6, number=511, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="OBUID", index=7, number=999, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=142,
    serialized_end=237,
)
_sym_db.RegisterEnumDescriptor(_ERRORCODE)

ErrorCode = enum_type_wrapper.EnumTypeWrapper(_ERRORCODE)
LTEV = 500
NET = 501
CPU = 502
MEM = 503
GPS = 504
MAP = 510
SPAT = 511
OBUID = 999


_OBUALARM = _descriptor.Descriptor(
    name="ObuAlarm",
    full_name="apollo.v2x.ObuAlarm",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="mode_num",
            full_name="apollo.v2x.ObuAlarm.mode_num",
            index=0,
            number=1,
            type=1,
            cpp_type=5,
            label=2,
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
        _descriptor.FieldDescriptor(
            name="error_num",
            full_name="apollo.v2x.ObuAlarm.error_num",
            index=1,
            number=2,
            type=14,
            cpp_type=8,
            label=2,
            has_default_value=False,
            default_value=500,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="error_msg",
            full_name="apollo.v2x.ObuAlarm.error_msg",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=2,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
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
    serialized_start=51,
    serialized_end=140,
)

_OBUALARM.fields_by_name["error_num"].enum_type = _ERRORCODE
DESCRIPTOR.message_types_by_name["ObuAlarm"] = _OBUALARM
DESCRIPTOR.enum_types_by_name["ErrorCode"] = _ERRORCODE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ObuAlarm = _reflection.GeneratedProtocolMessageType(
    "ObuAlarm",
    (_message.Message,),
    dict(
        DESCRIPTOR=_OBUALARM,
        __module__="modules.v2x.proto.v2x_monitor_pb2"
        # @@protoc_insertion_point(class_scope:apollo.v2x.ObuAlarm)
    ),
)
_sym_db.RegisterMessage(ObuAlarm)


# @@protoc_insertion_point(module_scope)
