from enum import Enum
from typing import List, Tuple
from abc import ABC, abstractmethod
from contract_bootloader.memorizer.evm.memorizer import EvmMemorizer
from marshmallow_dataclass import dataclass
from starkware.cairo.lang.vm.crypto import poseidon_hash_many
from starkware.cairo.lang.vm.relocatable import RelocatableValue


class EvmStateFunctionId(Enum):
    GET_STATUS = 0
    GET_CUMULATIVE_GAS_USED = 1
    GET_BLOOM = 2
    GET_LOGS = 3

    @classmethod
    def from_int(cls, value: int):
        if not isinstance(value, int):
            raise ValueError(f"Value must be an integer, got {type(value)}")
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")

    @classmethod
    def from_int(cls, value: int):
        if not isinstance(value, int):
            raise ValueError(f"Value must be an integer, got {type(value)}")
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")

    @classmethod
    def size(cls) -> int:
        return 1


@dataclass(frozen=True)
class MemorizerKey:
    chain_id: int
    block_number: int
    index: int

    @classmethod
    def from_int(cls, values: List[int]):
        if len(values) != cls.size():
            raise ValueError(
                "MemorizerKey must be initialized with a list of three integers"
            )
        return cls(values[0], values[1], values[2])

    def derive(self) -> int:
        return poseidon_hash_many([self.chain_id, self.block_number, self.index])

    def to_dict(self):
        return {
            "chain_id": self.chain_id,
            "block_number": self.block_number,
            "index": self.index,
        }

    @classmethod
    def size(cls) -> int:
        return 3


class AbstractEvmBlockReceiptBase(ABC):
    def __init__(self, memorizer: EvmMemorizer):
        self.memorizer = memorizer
        self.function_map = {
            EvmStateFunctionId.GET_STATUS: self.get_status,
            EvmStateFunctionId.GET_CUMULATIVE_GAS_USED: self.get_cumulative_gas_used,
            EvmStateFunctionId.GET_BLOOM: self.get_bloom,
            EvmStateFunctionId.GET_LOGS: self.get_logs,
        }

    def handle(
        self, function_id: EvmStateFunctionId, key: MemorizerKey
    ) -> Tuple[int, int]:
        if function_id in self.function_map:
            return self.function_map[function_id](key=key)
        else:
            raise ValueError(f"Function ID {function_id} is not recognized.")

    @abstractmethod
    def get_status(self, key: MemorizerKey) -> Tuple[int, int]:
        pass

    @abstractmethod
    def get_cumulative_gas_used(self, key: MemorizerKey) -> Tuple[int, int]:
        pass

    @abstractmethod
    def get_bloom(self, key: MemorizerKey) -> Tuple[int, int]:
        pass

    @abstractmethod
    def get_logs(self, key: MemorizerKey) -> Tuple[int, int]:
        pass

    def _get_felt_range(self, start_addr: int, end_addr: int) -> List[int]:
        assert isinstance(start_addr, RelocatableValue)
        assert isinstance(end_addr, RelocatableValue)
        assert start_addr.segment_index == end_addr.segment_index, (
            "Inconsistent start and end segment indices "
            f"({start_addr.segment_index} != {end_addr.segment_index})."
        )

        assert start_addr.offset <= end_addr.offset, (
            "The start offset cannot be greater than the end offset"
            f"({start_addr.offset} > {end_addr.offset})."
        )

        size = end_addr.offset - start_addr.offset
        return self.segments.memory.get_range_as_ints(addr=start_addr, size=size)
