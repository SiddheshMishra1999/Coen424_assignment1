# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protoFormat.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11protoFormat.proto\"h\n\x13responseForWorkload\x12\x0e\n\x06RFWDID\x18\x01 \x01(\t\x12\x13\n\x0bLastBatchID\x18\x02 \x01(\x05\x12\x15\n\rdataRequested\x18\x03 \x03(\x01\x12\x15\n\rdataAnalytics\x18\x04 \x01(\x01\"\xb3\x01\n\x12requestForWorkload\x12\x0e\n\x06RFWDID\x18\x01 \x01(\t\x12\x15\n\rbenchmarkType\x18\x02 \x01(\t\x12\x16\n\x0eworkloadMetric\x18\x03 \x01(\t\x12\x11\n\tbatchUnit\x18\x04 \x01(\x05\x12\x0f\n\x07\x62\x61tchID\x18\x05 \x01(\x05\x12\x11\n\tbatchSize\x18\x06 \x01(\x05\x12\x10\n\x08\x64\x61taType\x18\x07 \x01(\t\x12\x15\n\rdataAnalytics\x18\x08 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protoFormat_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _RESPONSEFORWORKLOAD._serialized_start=21
  _RESPONSEFORWORKLOAD._serialized_end=125
  _REQUESTFORWORKLOAD._serialized_start=128
  _REQUESTFORWORKLOAD._serialized_end=307
# @@protoc_insertion_point(module_scope)
