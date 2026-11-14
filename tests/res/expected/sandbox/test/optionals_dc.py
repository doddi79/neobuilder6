# md5: 1a08fc9200e22f1ebe77b7e2e0978513
# Auto-Generated file - DO NOT EDIT!
# Source module: sandbox.test.optionals_pb2
# Generated at: 2026-11-14T12:45:11.562162
from __future__ import annotations
__all__ = [
    'OptionalsMessage',
]
import dataclasses
import datetime
import enum
import typing
from protoplasm6.casting import dictators
from protoplasm6 import plasm
from sandbox.test import enums_dc as sandbox__test__enums_dc

from sandbox.test import optionals_pb2 as pb2

import logging
log = logging.getLogger(__name__)


@dataclasses.dataclass
class OptionalsMessage(plasm.DataclassBase):
    __proto_cls__ = pb2.OptionalsMessage
    maybe_double: typing.Optional[float] = dataclasses.field(default=None, metadata={'dictator': dictators.BaseDictator, 'is_optional': True})
    maybe_string: typing.Optional[str] = dataclasses.field(default=None, metadata={'dictator': dictators.BaseDictator, 'is_optional': True})
    maybe_long: typing.Optional[int] = dataclasses.field(default=None, metadata={'dictator': dictators.LongDictator, 'is_optional': True})
    maybe_bool: typing.Optional[bool] = dataclasses.field(default=None, metadata={'dictator': dictators.BaseDictator, 'is_optional': True})
    maybe_enum: typing.Optional[sandbox__test__enums_dc.ExternalEnum] = dataclasses.field(default=None, metadata={'dictator': dictators.EnumDictator, 'is_enum': True, 'is_optional': True})
    plain_double: float = dataclasses.field(default=0.0, metadata={'dictator': dictators.BaseDictator})
    choice_string: str = dataclasses.field(default='', metadata={'dictator': dictators.BaseDictator})
    choice_double: float = dataclasses.field(default=0.0, metadata={'dictator': dictators.BaseDictator})


