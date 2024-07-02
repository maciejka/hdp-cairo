from enum import Enum
import json
from typing import List, Optional, Union
from marshmallow import Schema
import marshmallow_dataclass
from dataclasses import asdict, field
import marshmallow.fields as mfields
from contract_bootloader.contract_class.contract_class import CompiledClass
from starkware.starkware_utils.validated_dataclass import ValidatedMarshmallowDataclass
from starkware.starkware_utils.marshmallow_dataclass_fields import (
    IntAsHex,
    additional_metadata,
)
from contract_bootloader.memorizer.account_memorizer import (
    MemorizerKey as AccountMemorizerKey,
)
from contract_bootloader.memorizer.header_memorizer import (
    MemorizerKey as HeaderMemorizerKey,
)


@marshmallow_dataclass.dataclass(frozen=True)
class ProcessedMPTProof:
    block_number: int
    proof: List[str]


@marshmallow_dataclass.dataclass(frozen=True)
class MMRMeta:
    id: int
    root: str
    size: int
    peaks: List[str] = field(
        metadata=additional_metadata(marshmallow_field=mfields.List(IntAsHex()))
    )


@marshmallow_dataclass.dataclass(frozen=True)
class HeaderProof:
    rlp: str
    leaf_idx: int
    mmr_path: List[str]


@marshmallow_dataclass.dataclass(frozen=True)
class AccountProof:
    address: str
    account_key: str
    proofs: List[ProcessedMPTProof]


@marshmallow_dataclass.dataclass(frozen=True)
class StorageProof:
    address: str
    slot: str
    storage_key: str
    proofs: List[ProcessedMPTProof]


@marshmallow_dataclass.dataclass(frozen=True)
class TransactionProof:
    key: str
    block_number: int
    proof: List[str]


@marshmallow_dataclass.dataclass(frozen=True)
class ReceiptProof:
    key: str
    block_number: int
    proof: List[str]


@marshmallow_dataclass.dataclass(frozen=True)
class Proofs(ValidatedMarshmallowDataclass):
    mmr_meta: MMRMeta
    headers: List[HeaderProof]
    accounts: List[AccountProof]
    storages: List[StorageProof]
    transactions: List[TransactionProof]
    transaction_receipts: List[ReceiptProof]


@marshmallow_dataclass.dataclass(frozen=True)
class Datalake:
    task_bytes_len: int
    encoded_task: List[int] = field(
        metadata=additional_metadata(marshmallow_field=mfields.List(IntAsHex()))
    )
    datalake_bytes_len: int
    encoded_datalake: List[int] = field(
        metadata=additional_metadata(marshmallow_field=mfields.List(IntAsHex()))
    )
    datalake_type: int
    property_type: int


@marshmallow_dataclass.dataclass(frozen=True)
class Module(ValidatedMarshmallowDataclass):
    inputs: List[int] = field(
        metadata=additional_metadata(
            marshmallow_field=mfields.List(IntAsHex(), required=True)
        )
    )
    module_class: CompiledClass


@marshmallow_dataclass.dataclass(frozen=True)
class DatalakeTask:
    datalake: Datalake


@marshmallow_dataclass.dataclass(frozen=True)
class ModuleTask:
    module: Module


@marshmallow_dataclass.dataclass(frozen=True)
class InputTask(ValidatedMarshmallowDataclass):
    task: Union[DatalakeTask, ModuleTask] = field(
        metadata=additional_metadata(marshmallow_field=mfields.Raw())
    )


@marshmallow_dataclass.dataclass(frozen=True)
class HDPInput(ValidatedMarshmallowDataclass):
    task_root: int = field(metadata=additional_metadata(marshmallow_field=IntAsHex()))
    proofs: Proofs
    tasks: List[InputTask] = field(
        metadata=additional_metadata(
            marshmallow_field=mfields.List(mfields.Nested(InputTask.Schema))
        )
    )
    result_root: Optional[int] = field(
        default=None, metadata=additional_metadata(marshmallow_field=IntAsHex())
    )


@marshmallow_dataclass.dataclass(frozen=True)
class HDPDryRunInput(ValidatedMarshmallowDataclass):
    dry_run_output_path: str
    modules: List[Module] = field(
        metadata=additional_metadata(
            marshmallow_field=mfields.List(mfields.Nested(Module.Schema))
        )
    )
