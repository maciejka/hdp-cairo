from hexbytes.main import HexBytes
from rlp import Serializable, decode
from rlp.sedes import Binary
from typing import List, Tuple

from tools.py.utils import little_8_bytes_chunks_to_bytes

bytes32 = Binary.fixed_length(32)

class Storage(Serializable):
    fields = (
        ("value", bytes32),
    )

    @property
    def value(self) -> HexBytes:
        return HexBytes(self._value)
    
    @classmethod
    def from_rpc_data(cls, value: HexBytes) -> 'Storage':
        return cls(value)
    
    @classmethod
    def from_rlp(cls, data: bytes) -> 'Storage':
        return decode(data, cls)
    
class FeltStorage:
    def __init__(self, storage: Storage):
        self.storage = storage

    @property
    def value(self) -> Tuple[int, int]:
        return self._split_to_felt(int.from_bytes(self.storage.value, 'big'))
    
    @classmethod
    def from_rlp_chunks(cls, value: HexBytes) -> 'FeltStorage':
        return cls(Storage(value))
    
    @classmethod
    def from_rpc_data(cls, data) -> 'FeltStorage':
        return cls(Storage.from_rpc_data(data))

    @classmethod
    def from_rlp_chunks(cls, rlp_chunks: List[int], rlp_len: int) -> 'FeltStorage':
        rlp = little_8_bytes_chunks_to_bytes(rlp_chunks, rlp_len)
        return cls(Storage.from_rlp(rlp))
    
