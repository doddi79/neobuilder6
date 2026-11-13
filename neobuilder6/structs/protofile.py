__all__ = [
    'ProtoFile',
]

import dataclasses
import os


@dataclasses.dataclass
class ProtoFile:  # E.g. ./proto/myshop/orders/billing/invoice.proto
    name: str  # E.g. invoice.proto
    path: str  # E.g. ./proto/myshop/orders/billing/
    rel_path: str  # E.g. myshop/orders/billing/
    is_grpc_service: bool = dataclasses.field(default=False)

    def full_name(self) -> str:
        return os.path.join(self.path, self.name).replace('\\', '/')

    def pb2_module(self) -> str:
        return f'{os.path.join(self.rel_path, self.name)[:-6].replace("/", ".")}_pb2'.replace('\\', '.')
