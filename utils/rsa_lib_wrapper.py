import rsa


from .encryption_utils import *


def encrypt_ecb(message: bytes, public_key: rsa.PublicKey) -> bytes:
    message_array = bytearray(message)
    block_size = int(public_key.n.bit_length() / 8) - 11
    blocks = divide_data_into_blocks(message_array, block_size)
    encrypted_blocks = list()
    for block in blocks:
        encrypted_blocks.append(rsa.encrypt(block, public_key))
    encrypted_message = b"".join(encrypted_blocks)
    return encrypted_message


def decrypt_ecb(message: bytes, private_key: rsa.PrivateKey) -> bytes:
    message_array = bytearray(message)
    block_size = int(private_key.n.bit_length() / 8)
    blocks = divide_data_into_blocks(message_array, block_size)
    decrypted_blocks = list()
    for block in blocks:
        decrypted_blocks.append(rsa.decrypt(block, private_key))
    decrypted_message = b"".join(decrypted_blocks)
    return decrypted_message


def encrypt_cbc(message: bytes, public_key: rsa.PublicKey) -> (bytes, int):
    message_array = bytearray(message)
    block_size = int(public_key.n.bit_length() / 8) - 11
    init_vector = create_random_init_vector(public_key.n.bit_length())
    previous_vector = init_vector.to_bytes(length=(public_key.n.bit_length()//8), byteorder="little")
    blocks = divide_data_into_blocks(message_array, block_size)
    encrypted_blocks = list()
    for block in blocks:
        block_as_number = int.from_bytes(block, "little")
        previous_vector_as_number = int.from_bytes(previous_vector[0:len(block)], byteorder="little")
        block = (block_as_number ^ previous_vector_as_number).to_bytes(length=len(block), byteorder="little")
        encrypted_block = rsa.encrypt(block, public_key)
        encrypted_blocks.append(encrypted_block)
        previous_vector = encrypted_block
    encrypted_message = b"".join(encrypted_blocks)
    return encrypted_message, init_vector


def decrypt_cbc(message: bytes, private_key: rsa.PrivateKey, init_vector: int) -> bytes:
    message_array = bytearray(message)
    block_size = int(private_key.n.bit_length() / 8)
    previous_vector = init_vector.to_bytes(length=(private_key.n.bit_length()//8), byteorder="little")
    blocks = divide_data_into_blocks(message_array, block_size)
    decrypted_blocks = list()
    for block in blocks:
        decrypted_block = rsa.decrypt(block, private_key)
        previous_vector_as_number = int.from_bytes(previous_vector[0:len(decrypted_block)], byteorder="little")
        decrypted_block_as_number = int.from_bytes(decrypted_block, "little")
        decrypted_block = (decrypted_block_as_number ^ previous_vector_as_number).to_bytes(length=len(decrypted_block),
                                                                                           byteorder="little")
        decrypted_blocks.append(decrypted_block)
        previous_vector = block
    decrypted_message = b"".join(decrypted_blocks)
    return decrypted_message


def private_key_to_rsa_data(key: rsa.PrivateKey):
    return RsaData(n=key.n, e=key.e, d=key.d, p=key.p, q=key.q)
