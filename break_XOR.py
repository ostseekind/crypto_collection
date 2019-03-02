import base64


# convert string to bits and print
def print_bits(a, b):
    # b'string' --> bytes object instead of ordinary string object
    # bin(byte) --> Byte to Bits
    # do that for each Byte of the input string
    # Example: bin1 = [bin(byte) for byte in b'test']
    # if variable is used: bytes(variable) to convert to bytes
    bin1 = [bin(byte) for byte in bytes(a, encoding='utf-8')]
    bin2 = [bin(byte) for byte in bytes(b, encoding='utf-8')]
    print(bin1)
    print(bin2)


# input: 2 strings,
# output: bytearray after XOR
def calculate_xor(a, b):
    # XOR difference
    # create byte list byte1 and byte2 --> XOR
    byte1 = [byte for byte in bytes(a, encoding='utf-8')]
    byte2 = [byte for byte in bytes(b, encoding='utf-8')]
    xor_bytes = [b1 ^ b2 for b1, b2 in zip(byte1, byte2)]
    return xor_bytes


# input: 2 strings
# calculate XOR, afterwards for each byte in XOR bytearray count number of '1' bits
# output: hamming weight (total number of '1' bits in XOR or input strings
def calculate_hamming(a, b):
    xor_bytes = calculate_xor(a, b)
    wt = 0
    for byte in xor_bytes:
        # for each bit in (convert byte to bit) if bit == 1
        wt += sum([1 for bit in bin(byte) if bit == '1'])
    return wt


# input: message (string), key (string)
# ensure key length = message length, calculate XOR and transform xor bytearray to string
# output: string (XOR encrypted/decrypted)
def encrypt_xor_test(m, k):
    len_m = len(m)
    len_k = len(k)
    # if message has more characters than key... extend key by concatenating with itself
    if len_m > len_k:
        q = round(len_m / len_k) + 1
        k = ''.join(k * q)
    # if key has more characters than message... cut key to correct size
    if len_m < len_k:
        k = k[:len_m]

    xor_bytes = calculate_xor(m, k)
    # convert to bytes
    # xor_bytes = [byte for byte in bytes(m, encoding='utf-8')]
    # convert int to character list
    str_x = [chr(byte) for byte in xor_bytes]
    # convert char list to string and print
    return ''.join(str_x)


def find_shortest_keysize(cipher):
    # dictionary list to store keysize with average wt
    avg_distances = []

    # iterate through possible keysizes
    for k_size in range(1, 41):
        # list to store distances
        distances = []
        # break ciphertext into chunks
        chunks = [cipher[i:i + k_size] for i in range(0, len(cipher) - k_size + 1, k_size)]

        for a_i in range(0, len(chunks)):
            for a_j in range(a_i, len(chunks)):
                if a_i + a_j < len(chunks):
                    chunk1 = chunks[a_i]
                    chunk2 = chunks[a_i + a_j]
                    wt = calculate_hamming(chunk1, chunk2)
                    distances.append(wt / k_size)

        if len(distances) != 0:
            result = {
                'key': k_size,
                'avg_distance': sum(distances) / len(distances)
            }
            avg_distances.append(result)

    # sorted(iterable[, key][, reverse])
    # lambda argument: manipulate(argument)
    # select first 3 elements (the ones with the lowest avg distance value)
    avg_dist_sorted = sorted(avg_distances, key=lambda x: x['avg_distance'])
    shortest_dist = (avg_dist_sorted[0], avg_dist_sorted[1], avg_dist_sorted[2])
    print("----------------------------------------------------------------------------------------")
    print("shortest distances: ")
    print("key1: " + str(shortest_dist[0]["key"]) + " -> distance: " + str(shortest_dist[0]["avg_distance"]))
    print("key2: " + str(shortest_dist[1]["key"]) + " -> distance: " + str(shortest_dist[1]["avg_distance"]))
    print("key3: " + str(shortest_dist[2]["key"]) + " -> distance: " + str(shortest_dist[2]["avg_distance"]))
    print("----------------------------------------------------------------------------------------")
    possible_k_sizes = (shortest_dist[0]["key"], shortest_dist[1]["key"], shortest_dist[2]["key"])
    return possible_k_sizes


def brute_force_char(cipher, k_size):
    # create chunks based on keysize
    keysize_chunks = [cipher[i:i + k_size] for i in range(0, len(cipher) - k_size + 1, k_size)]
    # traverse (get byte i from each chunk)
    traversed_blocks = []
    # store key
    key = []
    for i in range(0, k_size):
        block = ""
        for chunk_i in keysize_chunks:
            block += chunk_i[i]
        traversed_blocks.append(block)

    # for each traversed block brute force key byte
    for block in traversed_blocks:
        block = bytes(block, encoding='utf-8')
        possible_plain_chars = []
        # for each possible key byte...
        for possible_key_int in range(0, 255):
            # decrypt (for each byte in block -> XOR with possible key
            xor_bytes = b''
            for block_byte in block:
                xor_bytes += bytes([block_byte ^ possible_key_int])

            score = get_english_score(xor_bytes)
            # score = get_score(xor_bytes)
            data = {
                'plain_byte': xor_bytes,
                'score': score,
                'key_char': chr(possible_key_int)
            }
            possible_plain_chars.append(data)

        result = sorted(possible_plain_chars, key=lambda x: x['score'], reverse=True)[0]
        key.append(result["key_char"])

    key_string = ''.join(key)
    print("key: " + key_string)


# alternative to english score
def get_score(input_bytes):
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.'\n"
    point = 0
    for s in input_bytes:
        if chr(s) in charset or chr(s) == ' ' or chr(s) == '\'':
            point += 1
    return point


def get_english_score(input_bytes):
    """Compares each input byte to a character frequency
    chart and returns the score of a message based on the
    relative frequency the characters occur in the English
    language.
    """

    # From https://en.wikipedia.org/wiki/Letter_frequency
    # with the exception of ' ', which I estimated.
    character_frequencies = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .13000
    }
    return sum([character_frequencies.get(chr(byte), 0) for byte in input_bytes.lower()])


def test_hamming_calc():
    # input variables
    s1 = "this is a test"
    s2 = "wokka wokka!!!"

    # to test hamming calculation (should be 37 for "this is a test" and "wokka wokka!!!"
    distance = calculate_hamming(s1, s2)
    print("hamming distance = " + str(distance))


def get_xor_key(cipher):
    k_sizes = find_shortest_keysize(cipher)
    for size in k_sizes:
        print("---------------------------------------------")
        print("brute force for keysize = " + str(size))
        brute_force_char(cipher, size)
        print("---------------------------------------------")


def load_challenge6(filename):
    data = open(filename, "r").read()
    cipher = base64.b64decode(data)
    cipher = str(cipher, 'utf-8')
    # print(cipher)
    return cipher


def create_challenge(k):
    # read plaintext from file
    data = open("challenge-CFT-plain.txt", "r").read()
    # encrypt
    c = encrypt_xor_test(data, k)
    cipher_bytes = bytes(c, encoding='utf-8')
    cipher_base64 = base64.b64encode(cipher_bytes)
    # write encrypted base64 to file
    f = open("challenge-CFT-cipher.txt", "w")
    f.write(cipher_base64.decode('utf-8'))


if __name__ == "__main__":

    # to test hamming weight calculation
    # test_hamming_calc()

    plaintext = "And Another Thing ... will be the sixth novel in the now improbably named Hitchhiker's Guide to the Galaxy trilogy. Eight years after the death of its creator, Douglas Adams, the author's widow, Jane Belson, has given her approval for the project to be continued by the international number one bestselling children's writer, Eoin Colfer, author of the Artemis Fowl novels. Douglas Adams himself once said, 'I suspect at some point in the future I will write a sixth Hitchhiker book. Five seems to be a wrong kind of number, six is a better kind of number.' Belson said of Eoin Colfer, 'I love his books and could not think of a better person to transport Arthur, Zaphod and Marvin to pastures new.' Colfer, a fan of Hitchhiker since his schooldays, said, 'Being given the chance to write this book is like suddenly being offered the superpower of your choice. For years I have been finishing this incredible story in my head and now I have the opportunity to do it in the real world.' Prepare to be amazed"
    myKey = "This is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my keyThis is my k"

    # encrypt
    # c = encrypt_xor_test(plaintext, myKey)
    # print("Cipher: " + c)

    # c = load_challenge6("challenge6.txt")
    c = load_challenge6("challenge-CFT-cipher.txt")
    # brute force xor key (will be printed to stdout)
    get_xor_key(c)

    # key = "Terminator X: Bring the noise"
    key = "Imagine Dragons"
    p = encrypt_xor_test(c, key)
    print(p)

    # create_challenge("Imagine Dragons")

