# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modules/drivers/canbus/proto/can_card_parameter.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="modules/drivers/canbus/proto/can_card_parameter.proto",
    package="apollo.drivers.canbus",
    syntax="proto2",
    serialized_options=None,
    serialized_pb=_b(
        '\n5modules/drivers/canbus/proto/can_card_parameter.proto\x12\x15\x61pollo.drivers.canbus"\xa9\x05\n\x10\x43\x41NCardParameter\x12\x43\n\x05\x62rand\x18\x01 \x01(\x0e\x32\x34.apollo.drivers.canbus.CANCardParameter.CANCardBrand\x12\x41\n\x04type\x18\x02 \x01(\x0e\x32\x33.apollo.drivers.canbus.CANCardParameter.CANCardType\x12H\n\nchannel_id\x18\x03 \x01(\x0e\x32\x34.apollo.drivers.canbus.CANCardParameter.CANChannelId\x12G\n\tinterface\x18\x04 \x01(\x0e\x32\x34.apollo.drivers.canbus.CANCardParameter.CANInterface\x12\x14\n\tnum_ports\x18\x05 \x01(\r:\x01\x34"M\n\x0c\x43\x41NCardBrand\x12\x0c\n\x08\x46\x41KE_CAN\x10\x00\x12\x0b\n\x07\x45SD_CAN\x10\x01\x12\x12\n\x0eSOCKET_CAN_RAW\x10\x02\x12\x0e\n\nHERMES_CAN\x10\x03")\n\x0b\x43\x41NCardType\x12\x0c\n\x08PCI_CARD\x10\x00\x12\x0c\n\x08USB_CARD\x10\x01"\xb5\x01\n\x0c\x43\x41NChannelId\x12\x13\n\x0f\x43HANNEL_ID_ZERO\x10\x00\x12\x12\n\x0e\x43HANNEL_ID_ONE\x10\x01\x12\x12\n\x0e\x43HANNEL_ID_TWO\x10\x02\x12\x14\n\x10\x43HANNEL_ID_THREE\x10\x03\x12\x13\n\x0f\x43HANNEL_ID_FOUR\x10\x04\x12\x13\n\x0f\x43HANNEL_ID_FIVE\x10\x05\x12\x12\n\x0e\x43HANNEL_ID_SIX\x10\x06\x12\x14\n\x10\x43HANNEL_ID_SEVEN\x10\x07"2\n\x0c\x43\x41NInterface\x12\n\n\x06NATIVE\x10\x00\x12\x0b\n\x07VIRTUAL\x10\x01\x12\t\n\x05SLCAN\x10\x02'
    ),
)


_CANCARDPARAMETER_CANCARDBRAND = _descriptor.EnumDescriptor(
    name="CANCardBrand",
    full_name="apollo.drivers.canbus.CANCardParameter.CANCardBrand",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="FAKE_CAN", index=0, number=0, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="ESD_CAN", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="SOCKET_CAN_RAW", index=2, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="HERMES_CAN", index=3, number=3, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=406,
    serialized_end=483,
)
_sym_db.RegisterEnumDescriptor(_CANCARDPARAMETER_CANCARDBRAND)

_CANCARDPARAMETER_CANCARDTYPE = _descriptor.EnumDescriptor(
    name="CANCardType",
    full_name="apollo.drivers.canbus.CANCardParameter.CANCardType",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="PCI_CARD", index=0, number=0, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="USB_CARD", index=1, number=1, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=485,
    serialized_end=526,
)
_sym_db.RegisterEnumDescriptor(_CANCARDPARAMETER_CANCARDTYPE)

_CANCARDPARAMETER_CANCHANNELID = _descriptor.EnumDescriptor(
    name="CANChannelId",
    full_name="apollo.drivers.canbus.CANCardParameter.CANChannelId",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="CHANNEL_ID_ZERO",
            index=0,
            number=0,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="CHANNEL_ID_ONE", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="CHANNEL_ID_TWO", index=2, number=2, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="CHANNEL_ID_THREE",
            index=3,
            number=3,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="CHANNEL_ID_FOUR",
            index=4,
            number=4,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="CHANNEL_ID_FIVE",
            index=5,
            number=5,
            serialized_options=None,
            type=None,
        ),
        _descriptor.EnumValueDescriptor(
            name="CHANNEL_ID_SIX", index=6, number=6, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="CHANNEL_ID_SEVEN",
            index=7,
            number=7,
            serialized_options=None,
            type=None,
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=529,
    serialized_end=710,
)
_sym_db.RegisterEnumDescriptor(_CANCARDPARAMETER_CANCHANNELID)

_CANCARDPARAMETER_CANINTERFACE = _descriptor.EnumDescriptor(
    name="CANInterface",
    full_name="apollo.drivers.canbus.CANCardParameter.CANInterface",
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name="NATIVE", index=0, number=0, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="VIRTUAL", index=1, number=1, serialized_options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name="SLCAN", index=2, number=2, serialized_options=None, type=None
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=712,
    serialized_end=762,
)
_sym_db.RegisterEnumDescriptor(_CANCARDPARAMETER_CANINTERFACE)


_CANCARDPARAMETER = _descriptor.Descriptor(
    name="CANCardParameter",
    full_name="apollo.drivers.canbus.CANCardParameter",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="brand",
            full_name="apollo.drivers.canbus.CANCardParameter.brand",
            index=0,
            number=1,
            type=14,
            cpp_type=8,
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
            name="type",
            full_name="apollo.drivers.canbus.CANCardParameter.type",
            index=1,
            number=2,
            type=14,
            cpp_type=8,
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
            name="channel_id",
            full_name="apollo.drivers.canbus.CANCardParameter.channel_id",
            index=2,
            number=3,
            type=14,
            cpp_type=8,
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
            name="interface",
            full_name="apollo.drivers.canbus.CANCardParameter.interface",
            index=3,
            number=4,
            type=14,
            cpp_type=8,
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
            name="num_ports",
            full_name="apollo.drivers.canbus.CANCardParameter.num_ports",
            index=4,
            number=5,
            type=13,
            cpp_type=3,
            label=1,
            has_default_value=True,
            default_value=4,
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
        _CANCARDPARAMETER_CANCARDBRAND,
        _CANCARDPARAMETER_CANCARDTYPE,
        _CANCARDPARAMETER_CANCHANNELID,
        _CANCARDPARAMETER_CANINTERFACE,
    ],
    serialized_options=None,
    is_extendable=False,
    syntax="proto2",
    extension_ranges=[],
    oneofs=[],
    serialized_start=81,
    serialized_end=762,
)

_CANCARDPARAMETER.fields_by_name["brand"].enum_type = _CANCARDPARAMETER_CANCARDBRAND
_CANCARDPARAMETER.fields_by_name["type"].enum_type = _CANCARDPARAMETER_CANCARDTYPE
_CANCARDPARAMETER.fields_by_name[
    "channel_id"
].enum_type = _CANCARDPARAMETER_CANCHANNELID
_CANCARDPARAMETER.fields_by_name["interface"].enum_type = _CANCARDPARAMETER_CANINTERFACE
_CANCARDPARAMETER_CANCARDBRAND.containing_type = _CANCARDPARAMETER
_CANCARDPARAMETER_CANCARDTYPE.containing_type = _CANCARDPARAMETER
_CANCARDPARAMETER_CANCHANNELID.containing_type = _CANCARDPARAMETER
_CANCARDPARAMETER_CANINTERFACE.containing_type = _CANCARDPARAMETER
DESCRIPTOR.message_types_by_name["CANCardParameter"] = _CANCARDPARAMETER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CANCardParameter = _reflection.GeneratedProtocolMessageType(
    "CANCardParameter",
    (_message.Message,),
    dict(
        DESCRIPTOR=_CANCARDPARAMETER,
        __module__="modules.drivers.canbus.proto.can_card_parameter_pb2"
        # @@protoc_insertion_point(class_scope:apollo.drivers.canbus.CANCardParameter)
    ),
)
_sym_db.RegisterMessage(CANCardParameter)


# @@protoc_insertion_point(module_scope)
