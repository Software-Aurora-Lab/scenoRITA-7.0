# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modules/map/relative_map/proto/relative_map_config.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="modules/map/relative_map/proto/relative_map_config.proto",
    package="apollo.relative_map",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        '\n8modules/map/relative_map/proto/relative_map_config.proto\x12\x13\x61pollo.relative_map"\x7f\n\x12MapGenerationParam\x12 \n\x12\x64\x65\x66\x61ult_left_width\x18\x01 \x01(\x01:\x04\x31.75\x12!\n\x13\x64\x65\x66\x61ult_right_width\x18\x02 \x01(\x01:\x04\x31.75\x12$\n\x13\x64\x65\x66\x61ult_speed_limit\x18\x03 \x01(\x01:\x07\x32\x39.0576"\xaa\x04\n\x14NavigationLaneConfig\x12$\n\x17min_lane_marker_quality\x18\x01 \x01(\x01:\x03\x30.5\x12I\n\x0blane_source\x18\x02 \x01(\x0e\x32\x34.apollo.relative_map.NavigationLaneConfig.LaneSource\x12)\n\x1cmax_len_from_navigation_line\x18\x03 \x01(\x01:\x03\x32\x35\x30\x12(\n\x1bmin_len_for_navigation_lane\x18\x04 \x01(\x01:\x03\x31\x35\x30\x12(\n\x1bmax_len_for_navigation_lane\x18\x05 \x01(\x01:\x03\x32\x35\x30\x12-\n"ratio_navigation_lane_len_to_speed\x18\x06 \x01(\x01:\x01\x38\x12+\n\x1fmax_distance_to_navigation_line\x18\x07 \x01(\x01:\x02\x31\x35\x12.\n!min_view_range_to_use_lane_marker\x18\x08 \x01(\x01:\x03\x30.5\x12 \n\x13min_lane_half_width\x18\t \x01(\x01:\x03\x31.5\x12\x1e\n\x13max_lane_half_width\x18\n \x01(\x01:\x01\x32\x12\x1f\n\x12lane_marker_weight\x18\x0b \x01(\x01:\x03\x30.1"3\n\nLaneSource\x12\x0e\n\nPERCEPTION\x10\x01\x12\x15\n\x11OFFLINE_GENERATED\x10\x02"\x93\x01\n\x11RelativeMapConfig\x12:\n\tmap_param\x18\x01 \x01(\x0b\x32\'.apollo.relative_map.MapGenerationParam\x12\x42\n\x0fnavigation_lane\x18\x02 \x01(\x0b\x32).apollo.relative_map.NavigationLaneConfig'
    ),
)


_NAVIGATIONLANECONFIG_LANESOURCE = _descriptor.EnumDescriptor(
    name="LaneSource",
    full_name="apollo.relative_map.NavigationLaneConfig.LaneSource",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="PERCEPTION", index=0, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="OFFLINE_GENERATED",
            index=1,
            number=2,
            serialized_options=None,
            type=None,
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=714,
    serialized_end=765,
)
_sym_db.RegisterEnumDescriptor(_NAVIGATIONLANECONFIG_LANESOURCE)


_MAPGENERATIONPARAM = _descriptor.Descriptor(
    name="MapGenerationParam",
    full_name="apollo.relative_map.MapGenerationParam",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="default_left_width",
            full_name="apollo.relative_map.MapGenerationParam.default_left_width",
            index=0,
            number=1,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=True,
            default_value=float(1.75),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="default_right_width",
            full_name="apollo.relative_map.MapGenerationParam.default_right_width",
            index=1,
            number=2,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=True,
            default_value=float(1.75),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="default_speed_limit",
            full_name="apollo.relative_map.MapGenerationParam.default_speed_limit",
            index=2,
            number=3,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=True,
            default_value=float(29.0576),
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
    serialized_start=81,
    serialized_end=208,
)


_NAVIGATIONLANECONFIG = _descriptor.Descriptor(
    name="NavigationLaneConfig",
    full_name="apollo.relative_map.NavigationLaneConfig",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="min_lane_marker_quality",
            full_name="apollo.relative_map.NavigationLaneConfig.min_lane_marker_quality",
            index=0,
            number=1,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=True,
            default_value=float(0.5),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="lane_source",
            full_name="apollo.relative_map.NavigationLaneConfig.lane_source",
            index=1,
            number=2,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=1,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="max_len_from_navigation_line",
            full_name="apollo.relative_map.NavigationLaneConfig.max_len_from_navigation_line",
            index=2,
            number=3,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=True,
            default_value=float(250),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="min_len_for_navigation_lane",
            full_name="apollo.relative_map.NavigationLaneConfig.min_len_for_navigation_lane",
            index=3,
            number=4,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=True,
            default_value=float(150),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="max_len_for_navigation_lane",
            full_name="apollo.relative_map.NavigationLaneConfig.max_len_for_navigation_lane",
            index=4,
            number=5,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=True,
            default_value=float(250),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="ratio_navigation_lane_len_to_speed",
            full_name="apollo.relative_map.NavigationLaneConfig.ratio_navigation_lane_len_to_speed",
            index=5,
            number=6,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=True,
            default_value=float(8),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="max_distance_to_navigation_line",
            full_name="apollo.relative_map.NavigationLaneConfig.max_distance_to_navigation_line",
            index=6,
            number=7,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=True,
            default_value=float(15),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="min_view_range_to_use_lane_marker",
            full_name="apollo.relative_map.NavigationLaneConfig.min_view_range_to_use_lane_marker",
            index=7,
            number=8,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=True,
            default_value=float(0.5),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="min_lane_half_width",
            full_name="apollo.relative_map.NavigationLaneConfig.min_lane_half_width",
            index=8,
            number=9,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=True,
            default_value=float(1.5),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="max_lane_half_width",
            full_name="apollo.relative_map.NavigationLaneConfig.max_lane_half_width",
            index=9,
            number=10,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=True,
            default_value=float(2),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="lane_marker_weight",
            full_name="apollo.relative_map.NavigationLaneConfig.lane_marker_weight",
            index=10,
            number=11,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=True,
            default_value=float(0.1),
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
    enum_types=[
        _NAVIGATIONLANECONFIG_LANESOURCE,
    ],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=211,
    serialized_end=765,
)


_RELATIVEMAPCONFIG = _descriptor.Descriptor(
    name="RelativeMapConfig",
    full_name="apollo.relative_map.RelativeMapConfig",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="map_param",
            full_name="apollo.relative_map.RelativeMapConfig.map_param",
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
            name="navigation_lane",
            full_name="apollo.relative_map.RelativeMapConfig.navigation_lane",
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
    serialized_start=768,
    serialized_end=915,
)

_NAVIGATIONLANECONFIG.fields_by_name[
    "lane_source"
].enum_type = _NAVIGATIONLANECONFIG_LANESOURCE
_NAVIGATIONLANECONFIG_LANESOURCE.containing_type = _NAVIGATIONLANECONFIG
_RELATIVEMAPCONFIG.fields_by_name["map_param"].message_type = _MAPGENERATIONPARAM
_RELATIVEMAPCONFIG.fields_by_name[
    "navigation_lane"
].message_type = _NAVIGATIONLANECONFIG
DESCRIPTOR.message_types_by_name["MapGenerationParam"] = _MAPGENERATIONPARAM
DESCRIPTOR.message_types_by_name["NavigationLaneConfig"] = _NAVIGATIONLANECONFIG
DESCRIPTOR.message_types_by_name["RelativeMapConfig"] = _RELATIVEMAPCONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MapGenerationParam = _reflection.GeneratedProtocolMessageType(
    "MapGenerationParam",
    (_message.Message,),
    dict(
        DESCRIPTOR=_MAPGENERATIONPARAM,
        __module__="modules.map.relative_map.proto.relative_map_config_pb2"
        # @@protoc_insertion_point(class_scope:apollo.relative_map.MapGenerationParam)
    ),
)
_sym_db.RegisterMessage(MapGenerationParam)

NavigationLaneConfig = _reflection.GeneratedProtocolMessageType(
    "NavigationLaneConfig",
    (_message.Message,),
    dict(
        DESCRIPTOR=_NAVIGATIONLANECONFIG,
        __module__="modules.map.relative_map.proto.relative_map_config_pb2"
        # @@protoc_insertion_point(class_scope:apollo.relative_map.NavigationLaneConfig)
    ),
)
_sym_db.RegisterMessage(NavigationLaneConfig)

RelativeMapConfig = _reflection.GeneratedProtocolMessageType(
    "RelativeMapConfig",
    (_message.Message,),
    dict(
        DESCRIPTOR=_RELATIVEMAPCONFIG,
        __module__="modules.map.relative_map.proto.relative_map_config_pb2"
        # @@protoc_insertion_point(class_scope:apollo.relative_map.RelativeMapConfig)
    ),
)
_sym_db.RegisterMessage(RelativeMapConfig)


# @@protoc_insertion_point(module_scope)
