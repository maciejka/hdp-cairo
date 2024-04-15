from tools.py.utils import (
    bytes_to_8_bytes_chunks_little,
    split_128,
    reverse_endian_256,
    bytes_to_8_bytes_chunks,
    bytes_to_16_bytes_chunks,
)

tx_proof = [
    "f90131a0b07c76b82379b2847657563bc535e619929c7304b03e17b4885874ceb4aaedf3a08ceaeb43b2fe1d995d1d9a841a2e73d9bb3fc57212df497854a00ccb2dbc2da6a08d5107b60e0a57f5244ba18f7f80e33b573a9cb4213aad148f24bee4d4fb5230a0a59efeb29a395fe4a56e65f5cca6f66d33c0fce6d185006a4bbcef4c51076456a0e9257ff9f478a7e71e77ac7b1e06b7a6fcaaeca1b389f80f44b340d3b18b945ea0e7fcf7dad3e0c07edf83f0d4ac6276a3fb275f1a36d080305f135b178e56ba78a0659547369b68db130e5e623b7568f3d359521feb90506a9dadffc9f24b342274a0164d737b0d38dae9e6ea73abc4674d59b30677552157906d49123f3bc19c999fa03e002cd2bf1faea2741178a5aad431b6817fcac6af53ba5929ce4206f7b5de9b8080808080808080",
    "f851a06020738653830e8f898a391292dc660701a2ab357a64f77af201358c6b45b095a0b8bde0538fd4a46323823821ccdca1fd647016ea6449c7a91ac723a1585bc0ed808080808080808080808080808080",
    "f8d18080808080808080a0ac73e6a7aba0f884c60710d229dd3b7838caba6e22b7c2af93a0cadfe29f08c1a03b216831d2ec2ceddbc17cb84fc5e32c94f6e82f91dea0acb2272bf19ebea589a0e4ff974a860fe816692259a389537af757315c23f957224ad933a581dd89590da066df5e072b42ecdd20e5cecf1ee997ea7c549a0234b2a0a3cbf545cacfc0b384a0556cdae6413245b5638190bb0aa950ff4f0e3dd27a44f01ee55c056fcf6dbe24a033715a4f96ccde0167f1ab20c3465911e49de995f8dbcc4368093d8f3227c998808080",
    "f90211a003bf078edba62efe4e7cf6104a9dbd2a5f60f0acc60718c3384fce7d6f716c3ea075d2dfe513b541760394bf78781407fc3259319043fa6bf071645c4a6723ddb9a0e733f6a0b9e2a2ead847344c7e9927672b5051428f3efda9c09704befa53512ea052224da7adcd201ba47b775f4fb30fd0dd9a2a368748d85b1f1de99525eb78afa0e0dfcc2c2537dd355d58af3f7709870fff23aa9d04723125908d5df7ad1e68c9a09f3213f05d18f83ee1c69113157e0b08a226457a9c5c40427ce00dd34b57021da0c084a8afe364aa4745c2e3244d22fc464171197a6c11377b84cca36980200b7ca0eb97d2e2aa29258bb644d41516533c5bee1fe836463b88943db19fee129e0b68a0c4349f006f78e63aede3c7b00aa6ff55f739a0df109e100c1e5862b74facdabfa03250d9fec78f4f91bf99234e053d6f2669957084dae736b65c185d39278ef5c3a02dbb748fb688bce70ac5c52ea4239e5f1cc240e605357edfa693f3210bc32d6ea0de29bdfb334769ea97b9b25fd22e047122a47f48db54a4dce31bc080a1945950a0bf4e3475591edad458c9802e80f1b210765656c73b2176eff3b76fc9f33bfdfca00e4eaab5c3aa8bc61e40902d7204b78cdebe5445c3afd46c82f9df9f770605b4a0f5447edf0c9a17aa0553700c7803871e9206ab304d3d25106ed1bcb1c31cb69da0f538f27456f6edb31283899403e1b9bc171836041042e1f18416659dafa1d4a180",
    "f87820b87502f87201058402321262850fd724715f8252089407d03a66c2fd7b9e60b4ae1177ca439d967884bb872386f26fc1000080c080a0bc5b3c58d31f7c2669f0a845c2d91dec54591afe735f074423ef69cb6d9a3387a05b07a387267212c53fdb35cc60321a546ea207d77b028327d836d3c8764f6ebe"
]
# tx_index = 0x81CA
# tx_index = reverse_endian_256(tx_index)
# tx_index = split_128(tx_index)

                    # print("Tx Index:", tx_index)
# root = 0x49959fa04d6139d7223433113700ebc18108a87d7ed8e02d7b4fa3695e36f077
# root = reverse_endian_256(root)
# root = split_128(root)
# print("Root:", root)
# proof_bytes = [bytes.fromhex(proof_node) for proof_node in tx_proof]
# proof_bytes_len = [len(byte_proof) for byte_proof in proof_bytes]
# chunks = [bytes_to_8_bytes_chunks_little(proof_node) for proof_node in proof_bytes]
# print(chunks)
# print(proof_bytes_len)



# encoded_datalake = bytes.fromhex("000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000009eb09c00000000000000000000000000000000000000000000000000000000009eb100000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000035035b38da6a701c568545dcfcb03fcb875f56beddc4339bee47335c234581644b387f7f0d28db05ad5b092e1152fc70647d559cef220000000000000000000000")
# hex_fat = [hex(val) for val in bytes_to_16_bytes_chunks(encoded_datalake)]
# print("Output Fat:")
# print("Output Int:", bytes_to_16_bytes_chunks(encoded_datalake))
# print("Output Hex:", hex_fat)

# 02 f8 72 01058402321262850fd724715f8252089407d03a66c2fd7b9e60b4ae1177ca439d967884bb872386f26fc1000080c080a0bc5b3c58d31f7c2669f0a845c2d91dec54591afe735f074423ef69cb6d9a3387a05b07a387267212c53fdb35cc60321a546ea207d77b028327d836d3c8764f6ebe
# version = 0x02
# code = 0xf7 + len(data_len) = 0xf8
# data_len = 0x72

proof_2 = [
    "f90131a0b07c76b82379b2847657563bc535e619929c7304b03e17b4885874ceb4aaedf3a08ceaeb43b2fe1d995d1d9a841a2e73d9bb3fc57212df497854a00ccb2dbc2da6a08d5107b60e0a57f5244ba18f7f80e33b573a9cb4213aad148f24bee4d4fb5230a0a59efeb29a395fe4a56e65f5cca6f66d33c0fce6d185006a4bbcef4c51076456a0e9257ff9f478a7e71e77ac7b1e06b7a6fcaaeca1b389f80f44b340d3b18b945ea0e7fcf7dad3e0c07edf83f0d4ac6276a3fb275f1a36d080305f135b178e56ba78a0659547369b68db130e5e623b7568f3d359521feb90506a9dadffc9f24b342274a0164d737b0d38dae9e6ea73abc4674d59b30677552157906d49123f3bc19c999fa03e002cd2bf1faea2741178a5aad431b6817fcac6af53ba5929ce4206f7b5de9b8080808080808080",
    "f851a06020738653830e8f898a391292dc660701a2ab357a64f77af201358c6b45b095a0b8bde0538fd4a46323823821ccdca1fd647016ea6449c7a91ac723a1585bc0ed808080808080808080808080808080",
    "f9041a20b9041602f90412018322861280850b98f21e0b83029815946b75d8af000000e20b7a7ddf000ba900b4009a808515c7002e0f9a823aeaa63125dd63f10874f99cdbbb18410e7fc79dd32ff469f8f90386f9024994eaa63125dd63f10874f99cdbbb18410e7fc79dd3f90231a0000000000000000000000000000000000000000000000000000000000000001da0e629a3873b2edc434149348402890d970a76d9a3ae4de8e57541156dab274d10a00000000000000000000000000000000000000000000000000000000000000009a0348d2e5830c20f07ed9302299bcb5cd5a4c9931e292bf42e5466f557d2db1cd0a054f5b59dc9b5bb49000ab23a9d0a924c5cdd1733e5bebeadcb8611814450120ba00000000000000000000000000000000000000000000000000000000000000005a0263cae475013f53a7607366cbbeba4f0fec9fc1528d4e60a19af45776e01745ba086853267f2534b9eec92fd7a80680d7481e5e740ce8d21c54361341b3a3c1f14a0b39e9ba92c3c47c76d4f70e3bc9c3270ab78d2592718d377c8f5433a34d3470aa0000000000000000000000000000000000000000000000000000000000000000ba0a78b521343fce79b129d9bbe9bff921a08c8a8fde6ae24a7e159847b3ba54bb7a00000000000000000000000000000000000000000000000000000000000000008a0c247e5713292da7b6b8145ca699e5c90c1257a929a9b107aa7c7d211bc3a369ca0000000000000000000000000000000000000000000000000000000000000000fa05de84563fdc81a8663ce72466e3e1e667da5e6c8834c90c011812476ee214f3ca00000000000000000000000000000000000000000000000000000000000000014a02bfc01d3e1f55c0e56fdd7bc07c7b8dc1346e63f92436866e127d1fa813cda37f8dd94672fefac7f6e3017d9a2f1c14fe048191a24ce14f8c6a00000000000000000000000000000000000000000000000000000000000000008a00000000000000000000000000000000000000000000000000000000000000006a00000000000000000000000000000000000000000000000000000000000000007a00000000000000000000000000000000000000000000000000000000000000009a0000000000000000000000000000000000000000000000000000000000000000aa0000000000000000000000000000000000000000000000000000000000000000cf85994c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2f842a012231cd4c753cb5530a43a74c45106c24765e6f81dc8927d4f4be7e53315d5a8a0af863274be5681dd15c28b07cc44ec05c35b85e20483f94c782d341146ca0a9401a04889e13a3c91a4d55c7b23e9b9316c9027e9443da2108514873a2bca3547b72ea0657f6d15a2c21072a4185b220733d6f3fa199cac44ef99dfada99703546d305c"]

type_0_tx = "16850BA43B74008252089486116622FAD1EF07DBB44EF34CBBA722B3787E57874CBE73261D98008025A025039AF42BC0634AC99A66E75EA372CD5D96EA249F9760ED2819188C9A314676A02814F18AF3985A80F03C8A0D7C32C6D90B8C017FA390ABE8939F5D84524CD836"
type_1_tx = "018301160B850BC3FCAA9582523F94E25A329D385F77DF5D4ED56265BABE2B99A5436E8790323C93A997DD80C080A041AD1CE7F9902572C62D7154EAF81AC98E16FE5D0E93036DE72273474871EE85A003A70FBCE7C7BA9AE962820BD367AB7A83BA7689E6D5F61844F3172BB6419B9F"
type_2_tx = "01058402321262850fd724715f8252089407d03a66c2fd7b9e60b4ae1177ca439d967884bb872386f26fc1000080c080a0bc5b3c58d31f7c2669f0a845c2d91dec54591afe735f074423ef69cb6d9a3387a05b07a387267212c53fdb35cc60321a546ea207d77b028327d836d3c8764f6ebe"
type_3_tx = "018213CF85012A05F20085067BF3114E837A120094A8CB082A5A689E0D594D7DA1E2D72A3D63ADC1BD80B906A4701F58C50000000000000000000000000000000000000000000000000000000000071735856067108BA30E184D777A3FC833F37983F2E48C57A597785755811D2A027B220000000000000000000000000000000000000000000000000000000010B9BDD9000000000000000000000000000000000000000000000000000000000000000365EA057C6834D687253AF6DD58745C268070507CF1F701ED510B4092EAF93601805CA1E763747779C17F34899ACD3507BB5BA2E22DC2C4CD862EF27E1A1462610000000000000000000000000000000000000000000000000000000065F7F03A66B6785A423D7803BE31774427AA91DB5973E0534F28D1C2FED8A53B34231DC100000000000000000000000000000000000000000000000000000000000001200000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000717360000000000000000000000000000000000000000000000000000000065F7F08A0000000000000000000000000000000000000000000000000000000010B9C1C182C0740D3A41268DE6B52AC1EAEE241298824DB68122F8787CB7A5E732435259000000000000000000000000000000000000000000000000000000000000000452A2EB0E93CE6A696BBD597709A2C1DFD5D5C9318F9E9F08087A88712E4606C5FCA6BEE4022BD331455BD97FC8B1006091FABFF53A1F01F9E22EAC597641F4864AF974C95B6D000E82565B427812526EAACC1C69DBC24606EA0E691F4C477D3300000000000000000000000000000000000000000000000000000000000001400000000000000000000000000000000000000000000000000000000000000480000000000000000000000000000000000000000000000000000000000000031800000000000000000000000000000000000000000000800B0000000000000000000000000000000000000000000000000000000000000004856067108BA30E184D777A3FC833F37983F2E48C57A597785755811D2A027B2200000580000000000000000000000000000000000000800B000000000000000000000000000000000000000000000000000000000000000300000000000000000000000065F7F08A00000000000000000000000065F7F0D2000105800000000000000000000000000000000000008001000000000000000000000000000000000000000000000000000000000000000552A2EB0E93CE6A696BBD597709A2C1DFD5D5C9318F9E9F08087A88712E4606C50001058000000000000000000000000000000000000080010000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000400010580000000000000000000000000000000000000801100000000000000000000000000000000000000000000000000000000000000072B15A2246FE5C72065054CEB2B0E3EC0E0E8CC7C70C3651D54FB314F8563E72F000105800000000000000000000000000000000000008011000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000001058000000000000000000000000000000000000080080000000000000000000000000000000000000000000000000000000000000000792A32F10DB9C017A5D17EF7D3D2AAC295A76115C4F71AFC2670A95B96C906700001058000000000000000000000000000000000000080080000000000000000000000000000000000000000000000000000000000000001826C71922C8C0347C4CC9534E07489C1ABF737C329184DE5597F8D657AEC337C00010580000000000000000000000000000000000000800800000000000000000000000000000000000000000000000000000000000000029BACB83454043EBDCB629D77075CCFB129F154B44283B83FB1E6A3AB5430F25E0000000000000000000000000000000000000000000000000000000000000000000000000000009101398AB6798047B0214B7C3E3983DC26FF2EEC3316ED34BC31A4823453ED02EF9B37CA6A2AFDB55E9F07A563E263FEDF3CA3AA7DAA49CC7772C351F2925037D6F775A14F7704F2107748CC766AB5D777541584DBF70A49DE223170822E452DA6FB83A3EA567570639B3791B2496C7F0CBE620B664CD9C38487DE263F37394E93AC83103C0E5DB6702246A14E527F854F87000000000000000000000000000000C001E1A0015560DE5B6C2EDA4B74CFD91620C300829C9C15D290A68BF43B10FE91C365F980A030D1D9B80835D7E5368DD74549EE3CD47948DA17B07E4F98F42702726ADD470BA027EDA9A5B312C0EF4E7C3C1C48716642B20553ECEE0478B1F128E99CF5612095"

def get_tx_params(hex_str):
    tx_bytes = bytes.fromhex(hex_str)
    bytes_len = len(tx_bytes)
    chunks = bytes_to_8_bytes_chunks_little(tx_bytes)
    rlp_len = len(chunks)
    hex_chunks = [hex(chunk) for chunk in chunks]
    return {"rlp": hex_chunks, "rlp_len": rlp_len, "bytes_len": bytes_len}

print(get_tx_params(type_3_tx))

experiment = "02f87201058402321262850fd724715f8252089407d03a66c2fd7b9e60b4ae1177ca439d967884bb872386f26fc1000080c080a0bc5b3c58d31f7c2669f0a845c2d91dec54591afe735f074423ef69cb6d9a3387a05b07a387267212c53fdb35cc60321a546ea207d77b028327d836d3c8764f6ebe"