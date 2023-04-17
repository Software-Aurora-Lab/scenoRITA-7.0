# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modules/common/latency_recorder/proto/latency_record.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from modules.common.proto import (
    header_pb2 as modules_dot_common_dot_proto_dot_header__pb2,
)

DESCRIPTOR = _descriptor.FileDescriptor(
    name="modules/common/latency_recorder/proto/latency_record.proto",
    package="apollo.common",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        '\n:modules/common/latency_recorder/proto/latency_record.proto\x12\rapollo.common\x1a!modules/common/proto/header.proto"I\n\rLatencyRecord\x12\x12\n\nbegin_time\x18\x01 \x01(\x04\x12\x10\n\x08\x65nd_time\x18\x02 \x01(\x04\x12\x12\n\nmessage_id\x18\x03 \x01(\x04"\x85\x01\n\x10LatencyRecordMap\x12%\n\x06header\x18\x01 \x01(\x0b\x32\x15.apollo.common.Header\x12\x13\n\x0bmodule_name\x18\x02 \x01(\t\x12\x35\n\x0flatency_records\x18\x03 \x03(\x0b\x32\x1c.apollo.common.LatencyRecord"z\n\x0bLatencyStat\x12)\n\x0cmin_duration\x18\x01 \x01(\x04:\x13\x39\x32\x32\x33\x33\x37\x32\x30\x33\x36\x38\x35\x34\x37\x37\x35\x38\x30\x38\x12\x14\n\x0cmax_duration\x18\x02 \x01(\x04\x12\x15\n\raver_duration\x18\x03 \x01(\x04\x12\x13\n\x0bsample_size\x18\x04 \x01(\r"\xb5\x01\n\x0cLatencyTrack\x12\x46\n\rlatency_track\x18\x01 \x03(\x0b\x32/.apollo.common.LatencyTrack.LatencyTrackMessage\x1a]\n\x13LatencyTrackMessage\x12\x14\n\x0clatency_name\x18\x01 \x01(\t\x12\x30\n\x0clatency_stat\x18\x02 \x01(\x0b\x32\x1a.apollo.common.LatencyStat"\x9f\x01\n\rLatencyReport\x12%\n\x06header\x18\x01 \x01(\x0b\x32\x15.apollo.common.Header\x12\x31\n\x0c\x65\x32\x65s_latency\x18\x02 \x01(\x0b\x32\x1b.apollo.common.LatencyTrack\x12\x34\n\x0fmodules_latency\x18\x03 \x01(\x0b\x32\x1b.apollo.common.LatencyTrack'
    ),
    dependencies=[
        modules_dot_common_dot_proto_dot_header__pb2.DESCRIPTOR,
    ],
)


_LATENCYRECORD = _descriptor.Descriptor(
    name="LatencyRecord",
    full_name="apollo.common.LatencyRecord",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="begin_time",
            full_name="apollo.common.LatencyRecord.begin_time",
            index=0,
            number=1,
            type=4,
            cpp_type=4,
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
            name="end_time",
            full_name="apollo.common.LatencyRecord.end_time",
            index=1,
            number=2,
            type=4,
            cpp_type=4,
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
            name="message_id",
            full_name="apollo.common.LatencyRecord.message_id",
            index=2,
            number=3,
            type=4,
            cpp_type=4,
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=112,
    serialized_end=185,
)


_LATENCYRECORDMAP = _descriptor.Descriptor(
    name="LatencyRecordMap",
    full_name="apollo.common.LatencyRecordMap",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="header",
            full_name="apollo.common.LatencyRecordMap.header",
            index=0,
            number=1,
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
            name="module_name",
            full_name="apollo.common.LatencyRecordMap.module_name",
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
            name="latency_records",
            full_name="apollo.common.LatencyRecordMap.latency_records",
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=188,
    serialized_end=321,
)


_LATENCYSTAT = _descriptor.Descriptor(
    name="LatencyStat",
    full_name="apollo.common.LatencyStat",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="min_duration",
            full_name="apollo.common.LatencyStat.min_duration",
            index=0,
            number=1,
            type=4,
            cpp_type=4,
            label=1,
            has_default_value=True,
            default_value=9223372036854775808,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="max_duration",
            full_name="apollo.common.LatencyStat.max_duration",
            index=1,
            number=2,
            type=4,
            cpp_type=4,
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
            name="aver_duration",
            full_name="apollo.common.LatencyStat.aver_duration",
            index=2,
            number=3,
            type=4,
            cpp_type=4,
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
            name="sample_size",
            full_name="apollo.common.LatencyStat.sample_size",
            index=3,
            number=4,
            type=13,
            cpp_type=3,
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=323,
    serialized_end=445,
)


_LATENCYTRACK_LATENCYTRACKMESSAGE = _descriptor.Descriptor(
    name="LatencyTrackMessage",
    full_name="apollo.common.LatencyTrack.LatencyTrackMessage",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="latency_name",
            full_name="apollo.common.LatencyTrack.LatencyTrackMessage.latency_name",
            index=0,
            number=1,
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
            name="latency_stat",
            full_name="apollo.common.LatencyTrack.LatencyTrackMessage.latency_stat",
            index=1,
            number=2,
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=536,
    serialized_end=629,
)

_LATENCYTRACK = _descriptor.Descriptor(
    name="LatencyTrack",
    full_name="apollo.common.LatencyTrack",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="latency_track",
            full_name="apollo.common.LatencyTrack.latency_track",
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
    ],
    extensions=[],
    nested_types=[
        _LATENCYTRACK_LATENCYTRACKMESSAGE,
    ],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=448,
    serialized_end=629,
)


_LATENCYREPORT = _descriptor.Descriptor(
    name="LatencyReport",
    full_name="apollo.common.LatencyReport",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="header",
            full_name="apollo.common.LatencyReport.header",
            index=0,
            number=1,
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
            name="e2es_latency",
            full_name="apollo.common.LatencyReport.e2es_latency",
            index=1,
            number=2,
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
            name="modules_latency",
            full_name="apollo.common.LatencyReport.modules_latency",
            index=2,
            number=3,
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=632,
    serialized_end=791,
)

_LATENCYRECORDMAP.fields_by_name[
    "header"
].message_type = modules_dot_common_dot_proto_dot_header__pb2._HEADER
_LATENCYRECORDMAP.fields_by_name["latency_records"].message_type = _LATENCYRECORD
_LATENCYTRACK_LATENCYTRACKMESSAGE.fields_by_name[
    "latency_stat"
].message_type = _LATENCYSTAT
_LATENCYTRACK_LATENCYTRACKMESSAGE.containing_type = _LATENCYTRACK
_LATENCYTRACK.fields_by_name[
    "latency_track"
].message_type = _LATENCYTRACK_LATENCYTRACKMESSAGE
_LATENCYREPORT.fields_by_name[
    "header"
].message_type = modules_dot_common_dot_proto_dot_header__pb2._HEADER
_LATENCYREPORT.fields_by_name["e2es_latency"].message_type = _LATENCYTRACK
_LATENCYREPORT.fields_by_name["modules_latency"].message_type = _LATENCYTRACK
DESCRIPTOR.message_types_by_name["LatencyRecord"] = _LATENCYRECORD
DESCRIPTOR.message_types_by_name["LatencyRecordMap"] = _LATENCYRECORDMAP
DESCRIPTOR.message_types_by_name["LatencyStat"] = _LATENCYSTAT
DESCRIPTOR.message_types_by_name["LatencyTrack"] = _LATENCYTRACK
DESCRIPTOR.message_types_by_name["LatencyReport"] = _LATENCYREPORT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LatencyRecord = _reflection.GeneratedProtocolMessageType(
    "LatencyRecord",
    (_message.Message,),
    dict(
        DESCRIPTOR=_LATENCYRECORD,
        __module__="modules.common.latency_recorder.proto.latency_record_pb2"
        # @@protoc_insertion_point(class_scope:apollo.common.LatencyRecord)
    ),
)
_sym_db.RegisterMessage(LatencyRecord)

LatencyRecordMap = _reflection.GeneratedProtocolMessageType(
    "LatencyRecordMap",
    (_message.Message,),
    dict(
        DESCRIPTOR=_LATENCYRECORDMAP,
        __module__="modules.common.latency_recorder.proto.latency_record_pb2"
        # @@protoc_insertion_point(class_scope:apollo.common.LatencyRecordMap)
    ),
)
_sym_db.RegisterMessage(LatencyRecordMap)

LatencyStat = _reflection.GeneratedProtocolMessageType(
    "LatencyStat",
    (_message.Message,),
    dict(
        DESCRIPTOR=_LATENCYSTAT,
        __module__="modules.common.latency_recorder.proto.latency_record_pb2"
        # @@protoc_insertion_point(class_scope:apollo.common.LatencyStat)
    ),
)
_sym_db.RegisterMessage(LatencyStat)

LatencyTrack = _reflection.GeneratedProtocolMessageType(
    "LatencyTrack",
    (_message.Message,),
    dict(
        LatencyTrackMessage=_reflection.GeneratedProtocolMessageType(
            "LatencyTrackMessage",
            (_message.Message,),
            dict(
                DESCRIPTOR=_LATENCYTRACK_LATENCYTRACKMESSAGE,
                __module__="modules.common.latency_recorder.proto.latency_record_pb2"
                # @@protoc_insertion_point(class_scope:apollo.common.LatencyTrack.LatencyTrackMessage)
            ),
        ),
        DESCRIPTOR=_LATENCYTRACK,
        __module__="modules.common.latency_recorder.proto.latency_record_pb2"
        # @@protoc_insertion_point(class_scope:apollo.common.LatencyTrack)
    ),
)
_sym_db.RegisterMessage(LatencyTrack)
_sym_db.RegisterMessage(LatencyTrack.LatencyTrackMessage)

LatencyReport = _reflection.GeneratedProtocolMessageType(
    "LatencyReport",
    (_message.Message,),
    dict(
        DESCRIPTOR=_LATENCYREPORT,
        __module__="modules.common.latency_recorder.proto.latency_record_pb2"
        # @@protoc_insertion_point(class_scope:apollo.common.LatencyReport)
    ),
)
_sym_db.RegisterMessage(LatencyReport)


# @@protoc_insertion_point(module_scope)
