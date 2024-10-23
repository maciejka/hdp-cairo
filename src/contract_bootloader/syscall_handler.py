from typing import (
    Dict,
    Iterable,
)
from starkware.cairo.lang.vm.relocatable import RelocatableValue, MaybeRelocatable
from starkware.cairo.lang.vm.memory_segments import MemorySegmentManager
from contract_bootloader.syscall_handler_base import SyscallHandlerBase
from starkware.cairo.common.dict import DictManager
from starkware.cairo.common.structs import CairoStructProxy
from starkware.starknet.business_logic.execution.objects import CallResult
from contract_bootloader.memorizer.evm.memorizer import EvmStateId, EvmMemorizer
from contract_bootloader.memorizer.evm.header import (
    EvmStateFunctionId as EvmHeaderFunctionId,
    MemorizerKey as HeaderMemorizerKey,
)
from contract_bootloader.memorizer.evm.account import (
    EvmStateFunctionId as EvmAccountFunctionId,
    MemorizerKey as AccountMemorizerKey,
)
from contract_bootloader.memorizer.evm.storage import (
    EvmStateFunctionId as EvmStorageFunctionId,
    MemorizerKey as StorageMemorizerKey,
)
from contract_bootloader.memorizer.evm.block_tx import (
    EvmStateFunctionId as EvmBlockTxFunctionId,
    MemorizerKey as BlockTxMemorizerKey,
)
from contract_bootloader.syscall_memorizer_handler.evm.account_handler import (
    EvmAccountHandler,
)
from contract_bootloader.syscall_memorizer_handler.evm.header_handler import (
    EvmHeaderHandler,
)
from contract_bootloader.syscall_memorizer_handler.evm.storage_handler import (
    EvmStorageHandler,
)
from contract_bootloader.syscall_memorizer_handler.evm.block_tx_handler import (
    EvmBlockTxHandler,
)


class SyscallHandler(SyscallHandlerBase):
    """
    A handler for system calls; used by the BusinessLogic entry point execution.
    """

    def __init__(
        self,
        dict_manager: DictManager,
        segments: MemorySegmentManager,
    ):
        super().__init__(segments=segments, initial_syscall_ptr=None)
        self.syscall_counter: Dict[str, int] = {}
        self.dict_manager = dict_manager

    def set_syscall_ptr(self, syscall_ptr: RelocatableValue):
        assert self._syscall_ptr is None, "syscall_ptr is already set."
        self._syscall_ptr = syscall_ptr

    def allocate_segment(self, data: Iterable[MaybeRelocatable]) -> RelocatableValue:
        segment_start = self.segments.add()
        self.segments.write_arg(ptr=segment_start, arg=data)
        return segment_start

    def _allocate_segment_for_retdata(self, retdata: Iterable[int]) -> RelocatableValue:
        return self.allocate_segment(data=retdata)

    def _call_contract_helper(
        self, request: CairoStructProxy, syscall_name: str
    ) -> CallResult:
        calldata = self._get_felt_range(
            start_addr=request.calldata_start, end_addr=request.calldata_end
        )

        retdata = []

        memorizerId = EvmStateId.from_int(request.contract_address)
        if memorizerId == EvmStateId.Header:
            total_size = EvmMemorizer.size() + HeaderMemorizerKey.size()

            if len(calldata) != total_size:
                raise ValueError(
                    f"Memorizer read must be initialized with a list of {total_size} integers"
                )

            function_id = EvmHeaderFunctionId.from_int(request.selector)
            memorizer = EvmMemorizer(
                dict_raw_ptrs=calldata[0 : EvmMemorizer.size()],
                dict_manager=self.dict_manager,
            )

            idx = EvmMemorizer.size()
            key = HeaderMemorizerKey.from_int(
                calldata[idx : idx + HeaderMemorizerKey.size()]
            )

            handler = EvmHeaderHandler(
                segments=self.segments,
                memorizer=memorizer,
            )
            retdata = handler.handle(function_id=function_id, key=key)

        elif memorizerId == EvmStateId.Account:
            total_size = EvmMemorizer.size() + AccountMemorizerKey.size()

            if len(calldata) != total_size:
                raise ValueError(
                    f"Memorizer read must be initialized with a list of {total_size} integers"
                )

            function_id = EvmAccountFunctionId.from_int(request.selector)
            memorizer = EvmMemorizer(
                dict_raw_ptrs=calldata[0 : EvmMemorizer.size()],
                dict_manager=self.dict_manager,
            )

            idx = EvmMemorizer.size()
            key = AccountMemorizerKey.from_int(
                calldata[idx : idx + AccountMemorizerKey.size()]
            )

            handler = EvmAccountHandler(
                segments=self.segments,
                memorizer=memorizer,
            )
            retdata = handler.handle(function_id=function_id, key=key)

        elif memorizerId == EvmStateId.Storage:
            total_size = EvmMemorizer.size() + StorageMemorizerKey.size()

            if len(calldata) != total_size:
                raise ValueError(
                    f"Memorizer read must be initialized with a list of {total_size} integers"
                )

            function_id = EvmStorageFunctionId.from_int(request.selector)
            memorizer = EvmMemorizer(
                dict_raw_ptrs=calldata[0 : EvmMemorizer.size()],
                dict_manager=self.dict_manager,
            )
            print(memorizer.dict_ptr)

            idx = EvmMemorizer.size()
            key = StorageMemorizerKey.from_int(
                calldata[idx : idx + StorageMemorizerKey.size()]
            )

            handler = EvmStorageHandler(
                segments=self.segments,
                memorizer=memorizer,
            )
            retdata = handler.handle(function_id=function_id, key=key)
        elif memorizerId == EvmStateId.BlockTx:
            total_size = EvmMemorizer.size() + BlockTxMemorizerKey.size()

            if len(calldata) != total_size:
                raise ValueError(
                    f"Memorizer read must be initialized with a list of {total_size} integers"
                )

            function_id = EvmBlockTxFunctionId.from_int(request.selector)
            memorizer = EvmMemorizer(
                dict_raw_ptrs=calldata[0 : EvmMemorizer.size()],
                dict_manager=self.dict_manager,
            )

            idx = EvmMemorizer.size()
            key = BlockTxMemorizerKey.from_int(
                calldata[idx : idx + BlockTxMemorizerKey.size()]
            )

            handler = EvmBlockTxHandler(
                segments=self.segments,
                memorizer=memorizer,
            )
            retdata = handler.handle(function_id=function_id, key=key)

        else:
            raise ValueError(f"EvmStateId {memorizerId} not matched")

        return CallResult(
            gas_consumed=0,
            failure_flag=0,
            retdata=list(retdata),
        )
