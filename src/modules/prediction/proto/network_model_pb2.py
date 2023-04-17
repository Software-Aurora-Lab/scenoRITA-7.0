# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modules/prediction/proto/network_model.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from modules.prediction.proto import (
    network_layers_pb2 as modules_dot_prediction_dot_proto_dot_network__layers__pb2,
)

DESCRIPTOR = _descriptor.FileDescriptor(
    name="modules/prediction/proto/network_model.proto",
    package="apollo.prediction",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        '\n,modules/prediction/proto/network_model.proto\x12\x11\x61pollo.prediction\x1a-modules/prediction/proto/network_layers.proto"q\n\x12VerificationSample\x12\x34\n\x08\x66\x65\x61tures\x18\x01 \x03(\x0b\x32".apollo.prediction.TensorParameter\x12\x13\n\x0bprobability\x18\x02 \x01(\x02\x12\x10\n\x08\x64istance\x18\x03 \x01(\x02"B\n\x0bPerformance\x12\x10\n\x08\x61\x63\x63uracy\x18\x01 \x03(\x02\x12\x0e\n\x06recall\x18\x02 \x03(\x02\x12\x11\n\tprecision\x18\x03 \x03(\x02"\xea\x01\n\x0cNetParameter\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x31\n\x06layers\x18\x03 \x03(\x0b\x32!.apollo.prediction.LayerParameter\x12\x43\n\x14verification_samples\x18\x04 \x03(\x0b\x32%.apollo.prediction.VerificationSample\x12\x33\n\x0bperformance\x18\x05 \x01(\x0b\x32\x1e.apollo.prediction.Performance\x12\x13\n\x0btime_dumped\x18\x06 \x01(\x02'
    ),
    dependencies=[
        modules_dot_prediction_dot_proto_dot_network__layers__pb2.DESCRIPTOR,
    ],
)


_VERIFICATIONSAMPLE = _descriptor.Descriptor(
    name="VerificationSample",
    full_name="apollo.prediction.VerificationSample",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="features",
            full_name="apollo.prediction.VerificationSample.features",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
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
            name="probability",
            full_name="apollo.prediction.VerificationSample.probability",
            index=1,
            number=2,
            type=2,
            cpp_type=6,
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
        _descriptor.FieldDescriptor(
            name="distance",
            full_name="apollo.prediction.VerificationSample.distance",
            index=2,
            number=3,
            type=2,
            cpp_type=6,
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
    serialized_start=114,
    serialized_end=227,
)


_PERFORMANCE = _descriptor.Descriptor(
    name="Performance",
    full_name="apollo.prediction.Performance",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="accuracy",
            full_name="apollo.prediction.Performance.accuracy",
            index=0,
            number=1,
            type=2,
            cpp_type=6,
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
            name="recall",
            full_name="apollo.prediction.Performance.recall",
            index=1,
            number=2,
            type=2,
            cpp_type=6,
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
            name="precision",
            full_name="apollo.prediction.Performance.precision",
            index=2,
            number=3,
            type=2,
            cpp_type=6,
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=229,
    serialized_end=295,
)


_NETPARAMETER = _descriptor.Descriptor(
    name="NetParameter",
    full_name="apollo.prediction.NetParameter",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="id",
            full_name="apollo.prediction.NetParameter.id",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="name",
            full_name="apollo.prediction.NetParameter.name",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
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
        _descriptor.FieldDescriptor(
            name="layers",
            full_name="apollo.prediction.NetParameter.layers",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
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
            name="verification_samples",
            full_name="apollo.prediction.NetParameter.verification_samples",
            index=3,
            number=4,
            type=11,
            cpp_type=10,
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
            name="performance",
            full_name="apollo.prediction.NetParameter.performance",
            index=4,
            number=5,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="time_dumped",
            full_name="apollo.prediction.NetParameter.time_dumped",
            index=5,
            number=6,
            type=2,
            cpp_type=6,
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
    serialized_start=298,
    serialized_end=532,
)

_VERIFICATIONSAMPLE.fields_by_name[
    "features"
].message_type = (
    modules_dot_prediction_dot_proto_dot_network__layers__pb2._TENSORPARAMETER
)
_NETPARAMETER.fields_by_name[
    "layers"
].message_type = (
    modules_dot_prediction_dot_proto_dot_network__layers__pb2._LAYERPARAMETER
)
_NETPARAMETER.fields_by_name["verification_samples"].message_type = _VERIFICATIONSAMPLE
_NETPARAMETER.fields_by_name["performance"].message_type = _PERFORMANCE
DESCRIPTOR.message_types_by_name["VerificationSample"] = _VERIFICATIONSAMPLE
DESCRIPTOR.message_types_by_name["Performance"] = _PERFORMANCE
DESCRIPTOR.message_types_by_name["NetParameter"] = _NETPARAMETER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

VerificationSample = _reflection.GeneratedProtocolMessageType(
    "VerificationSample",
    (_message.Message,),
    dict(
        DESCRIPTOR=_VERIFICATIONSAMPLE,
        __module__="modules.prediction.proto.network_model_pb2"
        # @@protoc_insertion_point(class_scope:apollo.prediction.VerificationSample)
    ),
)
_sym_db.RegisterMessage(VerificationSample)

Performance = _reflection.GeneratedProtocolMessageType(
    "Performance",
    (_message.Message,),
    dict(
        DESCRIPTOR=_PERFORMANCE,
        __module__="modules.prediction.proto.network_model_pb2"
        # @@protoc_insertion_point(class_scope:apollo.prediction.Performance)
    ),
)
_sym_db.RegisterMessage(Performance)

NetParameter = _reflection.GeneratedProtocolMessageType(
    "NetParameter",
    (_message.Message,),
    dict(
        DESCRIPTOR=_NETPARAMETER,
        __module__="modules.prediction.proto.network_model_pb2"
        # @@protoc_insertion_point(class_scope:apollo.prediction.NetParameter)
    ),
)
_sym_db.RegisterMessage(NetParameter)


# @@protoc_insertion_point(module_scope)
