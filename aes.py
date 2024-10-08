import base64
import sys
import argparse
import os

rounds = 11

rcon = [
    0x8d,  # This is a placeholder and typically unused
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36,
    0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
    0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3,
    0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d,
    0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63,
    0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39,
    0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66,
    0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08,
    0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f,
    0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef,
    0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a,
    0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01,
    0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab,
    0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
    0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2,
    0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8,
    0xcb
]


sbox = [
    # 0     1    2     3    4     5    6     7    8     9    A     B    C     D    E     F
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,  # 0
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,  # 1
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,  # 2
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,  # 3
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,  # 4
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,  # 5
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,  # 6
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,  # 7
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,  # 8
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,  # 9
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,  # A
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,  # B
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,  # C
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,  # D
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,  # E
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16   # F
]


inv_sbox = [
    # 0     1    2     3     4     5     6     7    8     9    A     B    C     D    E     F
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,  # 0
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,  # 1
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,  # 2
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,  # 3
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,  # 4
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,  # 5
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,  # 6
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,  # 7
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,  # 8
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,  # 9
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,  # A
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,  # B
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,  # C
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,  # D
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,  # E
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d  # F
]


def key_expansion(key):

    key_schedule = [0] * rounds * 16
    for i in range(16):
        key_schedule[i] = key[i]

    for i in range(16, rounds * 16, 4):

        temp = key_schedule[i-4:i]

        if i % 16 == 0:
            temp = key_schedule_core(temp, i // 16)

        for j in range(4):
            key_schedule[i + j] = key_schedule[i + j - 16] ^ temp[j]

    return [key_schedule[i:i+16] for i in range(0, len(key_schedule) - 1, 16)]


def key_schedule_core(word, iteration):

    word = word[1:] + word[:1]

    word = [sbox[b] for b in word]

    word[0] ^= rcon[iteration]

    return word


def add_round_key(state, round_key_slice):
    return [(state[i] ^ round_key_slice[i]) for i in range(0, 16, 1)]


def sub_bytes(state):
    return [sbox[byte] for byte in state]


def shift_rows(state):

    state = [
        state[0], state[5], state[10], state[15], state[4], state[9], state[14], state[
            3], state[8], state[13], state[2], state[7], state[12], state[1], state[6], state[11]
    ]
    return state


def mix_columns(state):
    state_bkp = state.copy()
    for i in range(4):
        state[4*i] = (mul_by_2(state_bkp[4*i]) ^ mul_by_3(state_bkp[4*i + 1])
                      ^ state_bkp[4*i + 2] ^ state_bkp[4*i + 3]) & 0xFF
        state[4*i + 1] = (state_bkp[4*i] ^ mul_by_2(state_bkp[4*i + 1])
                          ^ mul_by_3(state_bkp[4*i + 2]) ^ state_bkp[4*i + 3]) & 0xFF
        state[4*i + 2] = (state_bkp[4*i] ^ state_bkp[4*i + 1] ^
                          mul_by_2(state_bkp[4*i + 2]) ^ mul_by_3(state_bkp[4*i + 3])) & 0xFF
        state[4*i+3] = (mul_by_3(state_bkp[4*i]) ^ state_bkp[4*i + 1]
                        ^ state_bkp[4*i + 2] ^ mul_by_2(state_bkp[4*i + 3])) & 0xFF
    return state


def mul_by_2(num):
    return ((num << 1) ^ (0x1B if num & 0x80 else 0)) & 0xFF


def mul_by_3(num):
    return (mul_by_2(num) ^ num) & 0xFF


def inv_shift_rows(state):

    state = [
        state[0], state[13], state[10], state[7], state[4], state[1], state[14], state[
            11], state[8], state[5], state[2], state[15], state[12], state[9], state[6], state[3]
    ]
    return state


def inv_sub_bytes(state):
    return [inv_sbox[byte] for byte in state]


def inv_mix_columns(state):
    state_bkp = state.copy()
    for i in range(4):
        state[4*i] = mul_by_e(state_bkp[4*i]) ^ mul_by_b(state_bkp[4*i + 1]
                                                         ) ^ mul_by_d(state_bkp[4*i + 2]) ^ mul_by_9(state_bkp[4*i + 3]) & 0xFF
        state[4*i + 1] = mul_by_9(state_bkp[4*i]) ^ mul_by_e(state_bkp[4*i + 1]
                                                             ) ^ mul_by_b(state_bkp[4*i + 2]) ^ mul_by_d(state_bkp[4*i + 3]) & 0xFF
        state[4*i + 2] = mul_by_d(state_bkp[4*i]) ^ mul_by_9(state_bkp[4*i + 1]
                                                             ) ^ mul_by_e(state_bkp[4*i + 2]) ^ mul_by_b(state_bkp[4*i + 3]) & 0xFF
        state[4*i + 3] = mul_by_b(state_bkp[4*i]) ^ mul_by_d(state_bkp[4*i + 1]
                                                             ) ^ mul_by_9(state_bkp[4*i + 2]) ^ mul_by_e(state_bkp[4*i + 3]) & 0xFF
    return state


def mul_by_9(num):
    return mul_by_2(mul_by_2(mul_by_2(num))) ^ num


def mul_by_b(num):
    return mul_by_2(mul_by_2(mul_by_2(num)) ^ num) ^ num


def mul_by_d(num):
    return mul_by_2(mul_by_2(mul_by_2(num) ^ num)) ^ num


def mul_by_e(num):
    return mul_by_2(mul_by_2(mul_by_2(num) ^ num) ^ num)


def aes_encrypt_block(state, key):

    global rounds
    round_keys = key_expansion(key)

    state = add_round_key(state, round_keys[0])

    for round in range(1, rounds - 1):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[round])

    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[rounds - 1])
    return state


def aes_decrypt_block(state, key):

    global rounds
    round_keys = key_expansion(key)
    state = add_round_key(state, round_keys[rounds - 1])
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    for i in range(rounds - 2, 0, -1):
        state = add_round_key(state, round_keys[i])
        state = inv_mix_columns(state)
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)

    state = add_round_key(state, round_keys[0])

    return state


def pad(plaintext, block_size=16):
    padding_len = block_size - (len(plaintext) % block_size)
    padding = bytes([padding_len] * padding_len)
    return plaintext + padding


def unpad(padded_data, block_size=16):
    padding_len = padded_data[-1]
    return padded_data[:-padding_len]


def aes_encrypt_ecb(plaintext, key):
    plaintext = pad(plaintext)
    ciphertext = []
    for i in range(0, len(plaintext) - 1, 16):
        ciphertext += aes_encrypt_block(plaintext[i:i+16], key)
    return ciphertext


def aes_decrypt_ecb(ciphertext, key):
    plaintext = []
    for i in range(0, len(ciphertext) - 1, 16):
        plaintext += aes_decrypt_block(ciphertext[i:i+16], key)
    plaintext = unpad(plaintext)
    return plaintext


def aes_encrypt_ctr(plaintext, key, nonce, counter):
    output_data = b''
    for i in range(0, len(plaintext) - 1, 16):
        counter_block = nonce + counter.to_bytes(8, 'big')
        keystream_block = aes_encrypt_block(counter_block, key)

        encrypted_block = bytes(
            a ^ b for a, b in zip(plaintext[i:i+16], keystream_block))

        output_data += encrypted_block
        counter += 1

    return output_data


def aes_decrypt_ctr(ciphertext, key, nonce, counter):
    output_data = b''

    for i in range(0, len(ciphertext) - 1, 16):
        block = ciphertext[i:i + 16]
        counter_block = nonce + counter.to_bytes(8, 'big')
        keystream_block = aes_encrypt_block(counter_block, key)

        decrypted_block = bytes(a ^ b for a, b in zip(block, keystream_block))
        output_data += decrypted_block
        counter += 1

    return output_data


def main():

    parser = argparse.ArgumentParser(
        description='Encrypt or decrypt a file using AES.')

    parser.add_argument('operation', type=str,
                        help='\"enc\" for encryption or \"dec\" for decryption')
    parser.add_argument('-rounds', type=int, required=True,
                        help='Number of rounds for AES encryption')
    parser.add_argument(
        '-key', type=str, required=True, help='Provide key as a sequence of hex numbers')
    parser.add_argument('-in_file', type=str, required=True,
                        help='Input file to be processed')
    parser.add_argument('-out_file', type=str,
                        required=True, help='Output file')
    parser.add_argument('-mode', type=str,
                        required=True, help='ecb or ctr')
    parser.add_argument('-iv', type=str,
                        required=False, help='nonce + counter start')

    args = parser.parse_args()

    global rounds
    rounds = args.rounds
    in_file = args.in_file
    out_file = args.out_file
    key = bytes.fromhex(args.key)
    operation = args.operation
    mode = args.mode
    nonce = bytes.fromhex(args.iv[0:16])
    counter = int(args.iv[16:])

    if mode == "ecb":
        if operation == "enc":
            with open(in_file, 'rb') as infile:
                plaintext = infile.read()
            ciphertext = aes_encrypt_ecb(plaintext, key)
            with open(out_file, 'wb') as outfile:
                outfile.write(bytes(ciphertext))
        elif operation == "dec":
            with open(in_file, 'rb') as infile:
                ciphertext = infile.read()
            plaintext = aes_decrypt_ecb(ciphertext, key)
            with open(out_file, 'wb') as outfile:
                outfile.write(bytes(plaintext))
    elif mode == "ctr":
        if operation == "enc":
            with open(in_file, 'rb') as infile:
                plaintext = infile.read()
            ciphertext = aes_encrypt_ctr(plaintext, key, nonce, counter)
            with open(out_file, 'wb') as outfile:
                outfile.write(bytes(ciphertext))
        elif operation == "dec":
            with open(in_file, 'rb') as infile:
                ciphertext = infile.read()
            plaintext = aes_decrypt_ctr(ciphertext, key, nonce, counter)
            with open(out_file, 'wb') as outfile:
                outfile.write(bytes(plaintext))


if __name__ == '__main__':
    main()
