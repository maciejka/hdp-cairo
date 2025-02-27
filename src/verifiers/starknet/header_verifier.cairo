from starkware.cairo.common.cairo_builtins import PoseidonBuiltin
from starkware.cairo.common.dict_access import DictAccess
from starkware.cairo.common.dict import dict_read
from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.builtin_poseidon.poseidon import poseidon_hash_many
from starkware.cairo.common.default_dict import default_dict_finalize
from packages.eth_essentials.lib.mmr import hash_subtree_path
from src.types import MMRMeta
from src.memorizers.starknet.memorizer import StarknetMemorizer, StarknetHashParams
from src.verifiers.mmr_verifier import validate_mmr_meta

func verify_mmr_batches{
    range_check_ptr,
    poseidon_ptr: PoseidonBuiltin*,
    pow2_array: felt*,
    starknet_memorizer: DictAccess*,
    mmr_metas: MMRMeta*,
    chain_id: felt,
}(mmr_meta_idx: felt) -> (mmr_meta_idx: felt) {
    alloc_locals;

    local mmr_batches_len: felt;
    %{ ids.mmr_batches_len = len(batch["mmr_with_headers"]) %}
    verify_mmr_batches_inner(mmr_batches_len, 0, mmr_meta_idx);

    return (mmr_meta_idx=mmr_meta_idx + mmr_batches_len);
}

// Check if the passed MMR meta is valid and if the headers are included in the MMR.
// Headers included in the MMR are memorized.
func verify_mmr_batches_inner{
    range_check_ptr,
    poseidon_ptr: PoseidonBuiltin*,
    pow2_array: felt*,
    mmr_metas: MMRMeta*,
    starknet_memorizer: DictAccess*,
    chain_id: felt,
}(mmr_batches_len: felt, idx: felt, mmr_meta_idx: felt) {
    alloc_locals;
    if (mmr_batches_len == idx) {
        return ();
    }

    %{
        vm_enter_scope({
               'mmr_batch': batch["mmr_with_headers"][ids.idx],
               '__dict_manager': __dict_manager
           })
    %}
    let (mmr_meta, peaks_dict, peaks_dict_start) = validate_mmr_meta(chain_id);
    assert mmr_metas[mmr_meta_idx + idx] = mmr_meta;

    local n_header_proofs: felt;
    %{ ids.n_header_proofs = len(mmr_batch["headers"]) %}
    with mmr_meta, peaks_dict {
        verify_headers_with_mmr_peaks(n_header_proofs);
    }
    %{ vm_exit_scope() %}

    // Ensure the peaks dict for this batch is finalized
    default_dict_finalize(peaks_dict_start, peaks_dict, -1);

    return verify_mmr_batches_inner(
        mmr_batches_len=mmr_batches_len, idx=idx + 1, mmr_meta_idx=mmr_meta_idx
    );
}

// Guard function that verifies the inclusion of headers in the MMR.
// It ensures:
// 1. The header hash is included in one of the peaks of the MMR.
// 2. The peaks dict contains the computed peak
// The peak checks are performed in isolation, so each MMR batch separatly.
// This ensures we dont create a bag of mmr peas from different chains, which are then used to check the header inclusion for every chain
func verify_headers_with_mmr_peaks{
    range_check_ptr,
    poseidon_ptr: PoseidonBuiltin*,
    pow2_array: felt*,
    mmr_meta: MMRMeta,
    starknet_memorizer: DictAccess*,
    peaks_dict: DictAccess*,
}(idx: felt) {
    alloc_locals;
    if (0 == idx) {
        return ();
    }

    let (fields) = alloc();
    local fields_len: felt;
    local leaf_idx: felt;
    %{
        header = mmr_batch["headers"][ids.idx - 1]
        segments.write_arg(ids.fields, hex_to_int_array(header["fields"]))
        ids.fields_len = len(header["fields"])
        ids.leaf_idx = header["proof"]["leaf_idx"]
    %}

    // compute the hash of the header
    let (header_hash) = poseidon_hash_many(n=fields_len, elements=fields);

    // a header can be the right-most peak
    if (leaf_idx == mmr_meta.size) {
        // instead of running an inclusion proof, we ensure its a known peak
        let (contains_peak) = dict_read{dict_ptr=peaks_dict}(header_hash);
        assert contains_peak = 1;

        // add to memorizer
        let block_number = [fields + 1];
        let memorizer_key = StarknetHashParams.header(mmr_meta.id, block_number);
        StarknetMemorizer.add(key=memorizer_key, data=fields);

        return verify_headers_with_mmr_peaks(idx=idx - 1);
    }

    let (mmr_path) = alloc();
    local mmr_path_len: felt;
    %{
        proof = header["proof"]
        segments.write_arg(ids.mmr_path, hex_to_int_array(proof["mmr_path"]))
        ids.mmr_path_len = len(proof["mmr_path"])
    %}

    // compute the peak of the header
    let (computed_peak) = hash_subtree_path(
        element=header_hash,
        height=0,
        position=leaf_idx,
        inclusion_proof=mmr_path,
        inclusion_proof_len=mmr_path_len,
    );

    // ensure the peak is included in the peaks dict, which contains the peaks of the mmr_root
    let (contains_peak) = dict_read{dict_ptr=peaks_dict}(computed_peak);
    assert contains_peak = 1;

    let block_number = [fields + 1];
    let memorizer_key = StarknetHashParams.header(mmr_meta.id, block_number);
    StarknetMemorizer.add(key=memorizer_key, data=fields);

    return verify_headers_with_mmr_peaks(idx=idx - 1);
}
