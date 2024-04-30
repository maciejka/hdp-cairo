from src.tasks.aggregate_functions.sum import compute_sum
from starkware.cairo.common.uint256 import (
    Uint256,
    felt_to_uint256,
    uint256_signed_div_rem,
    uint256_add,
)
from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.cairo_builtins import PoseidonBuiltin, BitwiseBuiltin, HashBuiltin

struct Output {
    result: Uint256,
}

func compute_regression{
    pedersen_ptr: HashBuiltin*,
    range_check_ptr,
    bitwise_ptr: BitwiseBuiltin*,
    poseidon_ptr: PoseidonBuiltin*,
}(values: Uint256*, values_len: felt) -> Uint256 {
    alloc_locals;

    // Inputs
    local input: felt* = cast(values, felt*);
    local input_size = values_len * 2;

    local return_ptr: felt*;
    %{ ids.return_ptr = segments.add() %}

    // TODO call run_simple_bootloader

    let output = cast(return_ptr - Output.SIZE, Output*);

    return (output.result);
}
