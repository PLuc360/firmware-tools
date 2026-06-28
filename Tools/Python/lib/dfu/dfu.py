import struct
import zlib

DEFAULT_DEVICE="0x0483:0xdf11"

def __compute_crc__(data):
    return 0xFFFFFFFF & -zlib.crc32(data) -1


def __build__(outputFile, targets, device=DEFAULT_DEVICE):
    data = []
    for t, target in enumerate(targets):
        tdata = []
        for image in target:
            tdata += struct.pack('<2I', image['address'], len(image['data'])) + image['data']
        tdata = [c for c in struct.pack('<6sBI255s2I', bytes('Target', 'utf-8'), 0, 1, bytes('ST...', 'utf-8'), len(tdata), len(target))] + tdata
        data += tdata
    data = [c for c in struct.pack('<5sBIB', bytes('DfuSe', 'utf-8'), 1, len(data) + 11, len(targets))] + data
    v, d = map(lambda x: int(x, 0) & 0xFFFF, device.split(':', 1))
    data += struct.pack('<4H3sB', 0, d, v, 0x011a, bytes('UFD', 'utf-8'), 16)
    crc = __compute_crc__(bytes(data))
    data += struct.pack('<I', crc)
    open(outputFile, 'wb').write(bytes(data))


def BuildDFU(outputFile, inputAddresses, inputFiles):
    target = []
    for idx in range((len(inputFiles))):
        address = int(inputAddresses[idx], 0) & 0xFFFFFFFF
        target.append({ 'address': address, 'data': open(inputFiles[idx],'rb').read() })

    __build__(outputFile, [target])