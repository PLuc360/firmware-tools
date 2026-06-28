def NumberToBytes(number, bytes_number):
    """ Serialize a number to a bytearray of bytes_number bytes (MSB first)

    Arguments:
    - number: [int] number to convert
    - bytes_number: [int] number of bytes to encode size

    Return:
    - result [byterarray]: serialized number
    """
    # check params
    assert isinstance(number, int)
    assert isinstance(bytes_number, int)

    result = []
    for idx in range(bytes_number):
        result.insert(0, (number >> (idx * 8)) & 0xFF)
    return result


def BytesToNumber(bytes_number, array):

    """ Deserialize a bytearray (MSB first) to a number

    Arguments:
    - bytes_number: [int] number of bytes to deserialize
    - array: [list] array to deserialize

    Return:
    - number: [int] deserialized number
    """

    # check params
    assert isinstance(bytes_number, int)
    assert isinstance(array, list)

    number = 0
    for idx in range(bytes_number):
        number += ((array[idx] & 0xFF) << ((bytes_number - idx - 1) * 8))

    return number

