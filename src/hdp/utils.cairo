from starkware.cairo.common.cairo_builtins import BitwiseBuiltin, KeccakBuiltin
from starkware.cairo.common.uint256 import Uint256, uint256_reverse_endian
from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.builtin_keccak.keccak import keccak
from starkware.cairo.common.keccak_utils.keccak_utils import keccak_add_uint256s
from src.libs.utils import felt_divmod
from src.libs.rlp_little import array_copy

from src.libs.utils import (
    word_reverse_endian_16_RC,
    word_reverse_endian_24_RC,
    word_reverse_endian_32_RC,
    word_reverse_endian_40_RC,
    word_reverse_endian_48_RC,
    word_reverse_endian_56_RC,
    word_reverse_endian_64,
)

// computes the result entry. This maps the result to a task_hash/id. It computes h(task_hash, result), which is a leaf in the results tree.
// Inputs:
// - task_hash: the task hash
// - result: the result
// Outputs:
// - the result entry
func compute_results_entry{
    range_check_ptr, bitwise_ptr: BitwiseBuiltin*, keccak_ptr: KeccakBuiltin*
}(task_hash: Uint256, result: Uint256) -> Uint256 {
    alloc_locals;

    // before hashing we need to reverse the endianness
    let (result_le) = uint256_reverse_endian(result);

    let (values_uint: Uint256*) = alloc();
    assert [values_uint] = task_hash;
    assert [values_uint + Uint256.SIZE] = result_le;

    let (values_felt) = alloc();
    let values_felt_start = values_felt;

    // convert to felts
    keccak_add_uint256s{
        range_check_ptr=range_check_ptr, bitwise_ptr=bitwise_ptr, inputs=values_felt
    }(n_elements=2, elements=values_uint, bigend=0);

    let (res_id) = keccak(values_felt_start, 64);

    return (res_id);
}

// reverses the endianness of chunk up to 56 bytes long
func reverse_small_chunk_endianess{range_check_ptr}(word: felt, bytes_len: felt) -> felt {
    if (bytes_len == 1) {
        return word;
    }
    if (bytes_len == 2) {
        return word_reverse_endian_16_RC{range_check_ptr=range_check_ptr}(word);
    }
    if (bytes_len == 3) {
        return word_reverse_endian_24_RC{range_check_ptr=range_check_ptr}(word);
    }
    if (bytes_len == 4) {
        return word_reverse_endian_32_RC{range_check_ptr=range_check_ptr}(word);
    }
    if (bytes_len == 5) {
        return word_reverse_endian_40_RC{range_check_ptr=range_check_ptr}(word);
    }
    if (bytes_len == 6) {
        return word_reverse_endian_48_RC{range_check_ptr=range_check_ptr}(word);
    }
    if (bytes_len == 7) {
        return word_reverse_endian_56_RC{range_check_ptr=range_check_ptr}(word);
    }

    assert 1 = 0;
    return 0;
}

func prepend_le_rlp_list_prefix{range_check_ptr, bitwise_ptr: BitwiseBuiltin*, pow2_array: felt*}(
    offset: felt, prefix: felt, rlp: felt*, rlp_len: felt
) -> (encoded: felt*, encoded_len: felt) {
    // we have no offset if the prefix is 0
    if (offset == 0) {
        return (encoded=rlp, encoded_len=rlp_len);
    }

    alloc_locals;
    let (local result: felt*) = alloc();

    let shifter = pow2_array[offset * 8];
    let devisor = pow2_array[(8 - offset) * 8];

    tempvar current_word = prefix;
    tempvar n_processed_words = 0;
    tempvar i = 0;

    loop:
    let i = [ap - 1];
    let n_processed_words = [ap - 2];
    let current_word = [ap - 3];

    %{ memory[ap] = 1 if (ids.rlp_len - ids.n_processed_words == 0) else 0 %}
    jmp end_loop if [ap] != 0, ap++;

    // Inlined felt_divmod (unsigned_div_rem).
    let q = [ap];
    let r = [ap + 1];
    %{
        ids.q, ids.r = divmod(memory[ids.rlp + ids.i], ids.devisor)
        #print(f"val={memory[ids.rlp + ids.i]} q={ids.q} r={ids.r} i={ids.i}")
    %}
    ap += 2;
    tempvar offset = 3 * n_processed_words;
    assert [range_check_ptr + offset] = q;
    assert [range_check_ptr + offset + 1] = r;
    assert [range_check_ptr + offset + 2] = devisor - r - 1;
    assert q * devisor + r = rlp[i];
    // done inlining felt_divmod.

    assert result[n_processed_words] = current_word + r * shifter;
    [ap] = q, ap++;
    [ap] = n_processed_words + 1, ap++;
    [ap] = i + 1, ap++;

    jmp loop;

    end_loop:
    assert rlp_len = n_processed_words;
    tempvar range_check_ptr = range_check_ptr + 3 * n_processed_words;

    // if the last word is not 0, we need to add it to the result and increment the rlp length
    if (current_word != 0) {
        assert result[n_processed_words] = current_word;
        return (encoded=result, encoded_len=rlp_len + 1);
    }
    return (encoded=result, encoded_len=rlp_len);

    // return (result);
}

// reverses the endianness of chunk, up to 64 bits long
func reverse_chunk_endianess{range_check_ptr, bitwise_ptr: BitwiseBuiltin*}(
    word: felt, bytes_len: felt
) -> felt {
    if (bytes_len == 1) {
        return word;
    }
    if (bytes_len == 2) {
        let res = word_reverse_endian_16_RC{range_check_ptr=range_check_ptr}(word);
        return (res);
    }
    if (bytes_len == 3) {
        let res = word_reverse_endian_24_RC{range_check_ptr=range_check_ptr}(word);
        return (res);
    }
    if (bytes_len == 4) {
        let res = word_reverse_endian_32_RC{range_check_ptr=range_check_ptr}(word);
        return (res);
    }
    if (bytes_len == 5) {
        let res = word_reverse_endian_40_RC{range_check_ptr=range_check_ptr}(word);
        return (res);
    }
    if (bytes_len == 6) {
        let res = word_reverse_endian_48_RC{range_check_ptr=range_check_ptr}(word);
        return (res);
    }
    if (bytes_len == 7) {
        let res = word_reverse_endian_56_RC{range_check_ptr=range_check_ptr}(word);
        return (res);
    }
    if (bytes_len == 8) {
        let (res) = word_reverse_endian_64{bitwise_ptr=bitwise_ptr}(word);
        return (res);
    }

    assert 1 = 0;
    return 0;
}

// Appends a BE 64-bit word to a list of 64-bit LE words, and returns the new list.
// Inputs:
// - list: the le chunks list to append to
// - list_bytes_len: the length of the list in bytes
// - item: the BE chunk to append (max 8 bytes)
// - item_bytes_len: the length of the item in bytes
func append_be_chunk{range_check_ptr, bitwise_ptr: BitwiseBuiltin*, pow2_array: felt*}(
    list: felt*, list_bytes_len: felt, chunk: felt, chunk_bytes_len: felt
) -> (list: felt*, list_len: felt, list_bytes_len: felt) {
    alloc_locals;

    let (word, offset) = felt_divmod(list_bytes_len, 8);
    let le_chunk = reverse_chunk_endianess{
        range_check_ptr=range_check_ptr, bitwise_ptr=bitwise_ptr
    }(chunk, chunk_bytes_len);

    if (offset == 0) {
        assert list[word] = le_chunk;
        return (list=list, list_len=word + 1, list_bytes_len=list_bytes_len + chunk_bytes_len);
    }

    // copy every element except the last one
    let (result) = alloc();
    array_copy(list, result, word, 0);

    // reverse and extend the chunk
    let le_extended = le_chunk * pow2_array[offset * 8];
    // %{
    //     print(f"le_chunk={hex(ids.le_chunk)} chunk={hex(ids.chunk)} chunk_bytes_len={ids.chunk_bytes_len}")
    // %}

    let (new_item, msb_item) = felt_divmod(le_extended, pow2_array[64]);
    assert result[word] = msb_item + list[word];

    // %{
    //     print(f"word_idx={ids.word} offset={ids.offset} last_word={hex(memory[ids.list + ids.word - 1])}")
    //     print(f"le_extended={hex(ids.le_extended)}")
    //     print(f"new_item={hex(ids.new_item)}")
    // %}

    if (new_item != 0) {
        assert result[word + 1] = new_item;
        return (list=result, list_len=word + 2, list_bytes_len=list_bytes_len + chunk_bytes_len);
    } else {
        return (list=result, list_len=word + 1, list_bytes_len=list_bytes_len + chunk_bytes_len);
    }

    // to simplyfy a maximum of 8 bytes can be added
    // assert [range_check_ptr] = 8 - chunk_bytes_len;

    // return ();
}
