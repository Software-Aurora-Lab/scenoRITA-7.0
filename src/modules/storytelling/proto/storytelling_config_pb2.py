# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modules/storytelling/proto/storytelling_config.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="modules/storytelling/proto/storytelling_config.proto",
    package="apollo.storytelling",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        '\n4modules/storytelling/proto/storytelling_config.proto\x12\x13\x61pollo.storytelling"L\n\x0bTopicConfig\x12!\n\x19planning_trajectory_topic\x18\x01 \x01(\t\x12\x1a\n\x12storytelling_topic\x18\x02 \x01(\t"L\n\x12StorytellingConfig\x12\x36\n\x0ctopic_config\x18\x01 \x01(\x0b\x32 .apollo.storytelling.TopicConfig'
    ),
)


_TOPICCONFIG = _descriptor.Descriptor(
    name="TopicConfig",
    full_name="apollo.storytelling.TopicConfig",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="planning_trajectory_topic",
            full_name="apollo.storytelling.TopicConfig.planning_trajectory_topic",
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
            name="storytelling_topic",
            full_name="apollo.storytelling.TopicConfig.storytelling_topic",
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=77,
    serialized_end=153,
)


_STORYTELLINGCONFIG = _descriptor.Descriptor(
    name="StorytellingConfig",
    full_name="apollo.storytelling.StorytellingConfig",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="topic_config",
            full_name="apollo.storytelling.StorytellingConfig.topic_config",
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
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=155,
    serialized_end=231,
)

_STORYTELLINGCONFIG.fields_by_name["topic_config"].message_type = _TOPICCONFIG
DESCRIPTOR.message_types_by_name["TopicConfig"] = _TOPICCONFIG
DESCRIPTOR.message_types_by_name["StorytellingConfig"] = _STORYTELLINGCONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TopicConfig = _reflection.GeneratedProtocolMessageType(
    "TopicConfig",
    (_message.Message,),
    dict(
        DESCRIPTOR=_TOPICCONFIG,
        __module__="modules.storytelling.proto.storytelling_config_pb2"
        # @@protoc_insertion_point(class_scope:apollo.storytelling.TopicConfig)
    ),
)
_sym_db.RegisterMessage(TopicConfig)

StorytellingConfig = _reflection.GeneratedProtocolMessageType(
    "StorytellingConfig",
    (_message.Message,),
    dict(
        DESCRIPTOR=_STORYTELLINGCONFIG,
        __module__="modules.storytelling.proto.storytelling_config_pb2"
        # @@protoc_insertion_point(class_scope:apollo.storytelling.StorytellingConfig)
    ),
)
_sym_db.RegisterMessage(StorytellingConfig)


# @@protoc_insertion_point(module_scope)
