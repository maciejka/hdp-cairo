%builtins range_check bitwise keccak
from starkware.cairo.common.alloc import alloc

from starkware.cairo.common.cairo_builtins import BitwiseBuiltin, KeccakBuiltin
from starkware.cairo.common.uint256 import Uint256, uint256_eq, uint256_reverse_endian
from starkware.cairo.common.keccak_utils.keccak_utils import keccak_add_uint256
from src.rlp import le_chunks_to_uint256, decode_rlp_word_to_uint256, rlp_list_retrieve, chunk_to_felt_be, right_shift_le_chunks
from packages.eth_essentials.lib.utils import pow2alloc127

func main{range_check_ptr, bitwise_ptr: BitwiseBuiltin*, keccak_ptr: KeccakBuiltin*}() {
    alloc_locals;
    let pow2_array: felt* = pow2alloc127();

    %{
        from tools.py.utils import (
            bytes_to_8_bytes_chunks_little,
            uint256_reverse_endian,
            split_128,
            reverse_endian,
            bytes_to_8_bytes_chunks,
        )
        import rlp
    %}

    test_decode_rlp_word_to_uint256{
        range_check_ptr=range_check_ptr, bitwise_ptr=bitwise_ptr, pow2_array=pow2_array
    }();
    test_rlp_list_retrieve{
        range_check_ptr=range_check_ptr, bitwise_ptr=bitwise_ptr, pow2_array=pow2_array
    }();
    test_chunk_to_felt_be{
        range_check_ptr=range_check_ptr, bitwise_ptr=bitwise_ptr, pow2_array=pow2_array
    }();
    test_right_shift_le_chunks{
        range_check_ptr=range_check_ptr, bitwise_ptr=bitwise_ptr, pow2_array=pow2_array
    }();

    return ();
}

func test_right_shift_le_chunks{
    range_check_ptr, bitwise_ptr: BitwiseBuiltin*, pow2_array: felt*
}() {
    alloc_locals;
    local elements_len: felt;

    %{
        input_values = [
            [0x1122334455667788, 0x11],
            [0x1122334455667788, 0x1122],
            [0x1122334455667788, 0x112233],
            [0x1122334455667788, 0x11223344],
            [0x1122334455667788, 0x1122334455],
            [0x1122334455667788, 0x112233445566],
            [0x1122334455667788, 0x11223344556677],
            [0x1122334455667788, 0x1122334455667788],
            [0x1122334455667788, 0x1122334455667788, 0x11],
        ]
        ids.elements_len = len(input_values)
        output_values = [
            [0x8800000000000000, 0x1111223344556677],
            [0x7788000000000000, 0x1122112233445566],
            [0x6677880000000000, 0x1122331122334455],
            [0x5566778800000000, 0x1122334411223344],
            [0x4455667788000000, 0x1122334455112233],
            [0x3344556677880000, 0x1122334455661122],
            [0x2233445566778800, 0x1122334455667711],
            [0x1122334455667788, 0x1122334455667788],
            [0x8800000000000000, 0x8811223344556677, 0x1111223344556677],
        ]
    
    %}

    test_test_right_shift_le_chunks(elements_len, 0);

    return ();
}

func test_test_right_shift_le_chunks{
    range_check_ptr, bitwise_ptr: BitwiseBuiltin*, pow2_array: felt*
}(elements_len: felt, index: felt) {
    alloc_locals;

    if(elements_len == index) {
        return ();
    }

    let (inputs: felt*) = alloc();
    local inputs_len: felt;
    local offset: felt;

    %{
        ids.offset = (9 + ids.index) % 8
        ids.inputs_len = len(input_values[ids.index])
        segments.write_arg(ids.inputs, input_values[ids.index])
    %}

    let (shifted) = right_shift_le_chunks(inputs, inputs_len, offset);

    %{
        for i in range(ids.inputs_len):
            assert memory[ids.shifted + i] == output_values[ids.index][i], f"Invalid Result at index {i}"        
    
    %}

    return test_test_right_shift_le_chunks(elements_len=elements_len, index=index + 1);
}


func test_chunk_to_felt_be{
    range_check_ptr, bitwise_ptr: BitwiseBuiltin*, pow2_array: felt*
}() {
    alloc_locals;   

    local elements_len: felt;

    %{
        values = [
            0xf,
            0xff,
            0xfff,
            0xffff,
            0xfffff,
            0xffffff,
            0xfffffff,
            0xffffffff,
            0xfffffffff,
            0xffffffffff,
            0xfffffffffff,
            0xffffffffffff,
            0xfffffffffffff,
            0xffffffffffffff,
        ]

        encoded_values = [rlp.encode(value) for value in values]
        chunks = [bytes_to_8_bytes_chunks_little(encoded_value) for encoded_value in encoded_values]

        ids.elements_len = len(values)
    %}

    return test_chunk_to_felt_be_inner(elements_len, 0);
}

func test_chunk_to_felt_be_inner{
    range_check_ptr, bitwise_ptr: BitwiseBuiltin*, pow2_array: felt*
}(elements_len: felt, index: felt) {
    alloc_locals;

    if(elements_len == index) {
        return ();
    }

    local value: felt;
    local expected: felt;
    %{ 
        ids.value = chunks[ids.index][0]
        ids.expected = values[ids.index]
    %}

    let result = chunk_to_felt_be(value);
    assert result = expected;

    return test_chunk_to_felt_be_inner(elements_len=elements_len, index=index + 1);
}

func test_rlp_list_retrieve{
    range_check_ptr, bitwise_ptr: BitwiseBuiltin*, pow2_array: felt*
}() {
    alloc_locals;

    local elements_len: felt;
    let (input_chunks: felt*) = alloc();
    local item_starts_at_byte: felt;

    %{
        # the list retrieve function selects elements by index, and then unpacks the element that is selected. This function mocks this
        def generate_encoded_results(elements):
            expected_results = []
            for element in elements:
                # Handle lists of elements (e.g., nested lists)
                if isinstance(element, list):
                    if len(element) == 0:
                        expected_results.append(b'\x00')
                    else:
                        # Encode each sub_element in the list using RLP and concatenate
                        encoded_concat = b''.join([rlp.encode(sub_element.to_bytes((sub_element.bit_length() + 7) // 8, byteorder='big')) for sub_element in element])
                        expected_results.append(encoded_concat)
                # Special handling for empty string or zero
                elif element == "" or element == 0:
                    expected_results.append(b'\x00')
                # Convert integers and large numbers to bytes
                else:
                    # Ensure integers are properly converted to bytes
                    num_bytes = (element.bit_length() + 7) // 8
                    element_bytes = element.to_bytes(num_bytes, byteorder='big')
                    # Append the result after encoding if needed
                    expected_results.append(element_bytes)
            return expected_results

        elements = [
            # empty
            '',
            # zero
            0x0, 
            #one byte
            1,
            0x7f, 
            # short string
            0x80,
            0xabcdef,
            0x55FE002aefF02F77364de339a1292923A15844B8,
            0xc84ed1f6941cc0826996633d523ccbf62c9a4417f377706d12d422f9def4ba6d,
            # long string 
            0xc84ed1f6941cc0826996633d523ccbf62c9a4417f377706d12d422f9def4ba6dc84ed1f6941cc0826996633d523ccbf62c9a4417f377706d12d422f9def4ba6d,
            # empty list
            [],
            # short list
            [0x0, 0x1],
            [0x55FE002aefF02F77364de339a1292923A15844B8, 0x55FE002aefF02F77364de339a1292923A15844B8, 0x55FE002aefF02F77364de3], # 55 bytes (with elements prefix)
            # long list
            [0xc84ed1f6941cc0826996633d523ccbf62c9a4417f377706d12d422f9def4ba6d, 0xc84ed1f6941cc0826996633d523ccbf62c9a4417f377706d12d422f9def4ba6d],
        ]

        # raw encoded element
        encoded_blob = rlp.encode(elements)

        input_chunks = bytes_to_8_bytes_chunks_little(encoded_blob)
        segments.write_arg(ids.input_chunks, input_chunks)
        ids.item_starts_at_byte = 3 # the first 3 bytes are the list prefix, which we want to skip
        ids.elements_len = len(elements)
        
        encoded_elements = generate_encoded_results(elements)
        expected_bytes_len = [len(element) for element in encoded_elements]
        expected_results = [bytes_to_8_bytes_chunks_little(result) for result in encoded_elements]
        expected_len =  [len(element) for element in expected_results]
    %}

    test_rlp_list_retrieve_inner{
        range_check_ptr=range_check_ptr, bitwise_ptr=bitwise_ptr, pow2_array=pow2_array, input_chunks=input_chunks, item_starts_at_byte=item_starts_at_byte
    }(elements_len, 0);

    return ();

}

func test_rlp_list_retrieve_inner{
    range_check_ptr, bitwise_ptr: BitwiseBuiltin*, pow2_array: felt*, input_chunks: felt*, item_starts_at_byte: felt
}(elements_len: felt, index: felt) {
    alloc_locals;

    if(elements_len == index) {
        return ();
    }

    let (result, result_len, result_bytes_len) = rlp_list_retrieve(
        input_chunks, index, item_starts_at_byte, 0
    );

    %{
        assert ids.result_len == expected_len[ids.index], "Invalid Results Length"
        assert ids.result_bytes_len == expected_bytes_len[ids.index], "Invalid Results Bytes Length"

        for i in range(ids.result_len):
            assert memory[ids.result + i] == expected_results[ids.index][i], f"Invalid Result at index {i}"

    %}


    return test_rlp_list_retrieve_inner(elements_len=elements_len, index=index + 1);
}

func test_decode_rlp_word_to_uint256{
    range_check_ptr, bitwise_ptr: BitwiseBuiltin*, pow2_array: felt*
}() {
    alloc_locals;

    local case_len: felt;
    %{
        # Test cases for decode_rlp_word_to_uint256 at every byte length
        decode_rlp_word_to_uint256 = [
            0x66,
            0x9388,
            0xae5e8a,
            0x4e98ca05,
            0x61cb9c7ce6,
            0x7211a2516f35,
            0x58b5d8b3f67446,
            0x7519e8621ea1a3ee,
            0x9ee2e781a323050f12,
            0xae45d19ed5310e62f4f3,
            0xf3fc1e528b85432aab4d45,
            0x43bc24aed589d97fae233712,
            0x97f3eab6553c2f284d04e314bd,
            0xb5f421d6740127fafbb0a89a8bc3,
            0x59309a988582ff574bd3ed9a4bd6ce,
            0x696b085c5dc084660c1903ed46d07456,
            0x895613670f5cedbba5d22dc9dc9e47fe1d,
            0xc33d466640180017ddeb18aacde8790775fd,
            0x4e6184f5eae2a03db9aeb583ec012b310894fc,
            0x183311ee3de03a9fdf7e30da707cea7842344095,
            0xa5a0abe55971873d59c8eacc1b0e3dc75d041a0560,
            0x8966bfd6beb8ad6f93bdaf78b87d8e0b7a0d55cb6608,
            0x65f51a126b8b9168089697ad4a978861a1df6ac779d8f2,
            0x719a99b4d93f830e3a12d8b21d8406bf673ededb3d74f835,
            0x7fb90265c0558fda3544677e3ac6bee21be6b0666686e8e886,
            0xd485c055420d72665e38f63657eeff26ea7a4cf658ad90ec433a,
            0xf427f5d9e55db2ca6cbc480c58ef030f1f9f3989e99b35c8ae176e,
            0xb39e496e6b029417ae37d000b3b86427e5bb366a738c3b1268ea15ff,
            0x938f32171b29d0e29d347e283edb0749d43dafcbff79cafc08f6e936c4,
            0x5a8fdd9d1017e051bda2cf1d27518c38714f0659dd8c362840f0aacf0b46,
            0x85bdc29d6de8c62e3c3a7789448dfa47cc2ad137791dcb6f7413fc1e347734,
            0x66ba7c97a8d86016687269a255b6557ae499a417222aede48aca47e8a34fccc8
        ]

        ids.case_len = len(decode_rlp_word_to_uint256)
    %}
    
    test_decode_rlp_word_to_uint256_inner{
        range_check_ptr=range_check_ptr, bitwise_ptr=bitwise_ptr, pow2_array=pow2_array
    }(case_len, 0);

    return ();
}

func test_decode_rlp_word_to_uint256_inner{
    range_check_ptr, bitwise_ptr: BitwiseBuiltin*, pow2_array: felt*
}(case_len: felt, index: felt) {
    alloc_locals;

    if (index == case_len) {
        return ();
    }

    let (chunks: felt*) = alloc();
    local expected_le: Uint256;
    local expected_be: Uint256;
    local bytes_len: felt;

    %{
        # Writes input and expected value to cairo
        def write_case_values(value):
            (low_be, high_be) = split_128(value)
            ids.expected_be.low = low_be
            ids.expected_be.high = high_be

            reversed_value = uint256_reverse_endian(value)
            (low_le, high_le) = split_128(reversed_value)
            ids.expected_le.low = low_le
            ids.expected_le.high = high_le

            rlp_value = rlp.encode(value)
            ids.bytes_len = len(rlp_value)
            chunks = bytes_to_8_bytes_chunks_little(rlp_value)
            segments.write_arg(ids.chunks, chunks)  

        write_case_values(decode_rlp_word_to_uint256[ids.index])
    %}

    let result_le = decode_rlp_word_to_uint256(chunks, bytes_len);
    let (local result_be) = uint256_reverse_endian(result_le);

    assert expected_le.low = result_le.low;
    assert expected_le.high = result_le.high;

    assert expected_be.low = result_be.low;
    assert expected_be.high = result_be.high;

    return test_decode_rlp_word_to_uint256_inner(case_len=case_len, index=index + 1);
}
