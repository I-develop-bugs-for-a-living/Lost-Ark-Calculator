from scapy.all import *
import snappy
from pathlib import Path
from array import array
from oodle import oodle

#opcodes = [48163, 53341, 32939, 2351, 17477, 26889, 36952, 194, 12348, 35843]
opcodes = [18842]


with open(Path('assets', 'xor.bin'), 'rb') as f:
    xorkey = f.read()


class hexdump:
    def __init__(self, buf, off=0):
        self.buf = buf
        self.off = off

    def __iter__(self):
        last_bs, last_line = None, None
        for i in range(0, len(self.buf), 16):
            bs = bytearray(self.buf[i : i + 16])
            line = "{:08x}  {:23}  {:23}  |{:16}|".format(
                self.off + i,
                " ".join(("{:02x}".format(x) for x in bs[:8])),
                " ".join(("{:02x}".format(x) for x in bs[8:])),
                "".join((chr(x) if 32 <= x < 127 else "." for x in bs)),
            )
            if bs == last_bs:
                line = "*"
            if bs != last_bs or line != last_line:
                yield line
            last_bs, last_line = bs, line
        yield "{:08x}".format(self.off + len(self.buf))

    def __str__(self):
        return "\n".join(self)

    def __repr__(self):
        return "\n".join(self)


def process_packet(packet):
    p = bytes(packet[TCP].payload)
    #print(f"Raw Packet: {p}\n")
    packet_size = int.from_bytes(p[0:1], "little")
    opcode = int.from_bytes(p[4:6], "little")
    if opcode in opcodes:
        print(f"OpCode: {opcode}")
        print(p)
        # payload = array('B', p[6:packet_size])
        # payload_final = oodle.decompress(payload)[16:]
        try:
            print()
            print(f"OpCode Found! {opcode}\n")
            print(f"Packet Size: {packet_size}\n")
            print(f"Raw Packet: {p}\n")
            payload = array('B', p[6:packet_size])
            print(f"Trimmed: {payload}\n")
            xor_cipher(payload, opcode, xorkey)
            print(f"Decrypted: {payload}\n")      
            compression_type = int.from_bytes(p[6:7], "little") 
            print(f"Compression Type: {int.from_bytes(p[6:7], 'little')}\n")
            match compression_type:
                case 0: # None
                    payload_final = payload[16:]
                case 1: # TODO: L4Z
                    raise RuntimeError('L4Z')
                case 2: # Snappy
                    print(f"Compression Type: Snappy\n")
                    payload_final = snappy.decompress(bytes(payload))
                case 3: # Oodle
                    print(f"Compression Type: Oodle\n")
                    payload_final = oodle.decompress(bytes(payload))[16:]
                case _: # ?????
                    raise RuntimeError('Unknown Compression Type')            
            print(f"Decompressed: {list(payload_final)}\n")
            print(f"Hex Dump: ")
            print(f"{hexdump(payload_final)}\n")
            if opcode == 48163:        
                price = int.from_bytes(payload_final[140:144], "little")
                quantity = int.from_bytes(payload_final[136:140], "little")
                print(f"Price: {price}, Quantity: {quantity}\n")
        except Exception as e:
            print(f"Error: {opcode}\n + {e}\n")

 
def xor_cipher(data, seed, xor_key):
    for i in range(len(data)):
        data[i] = data[i] ^ xor_key[seed % len(xor_key)]
        if i < len(data):
            seed += 1

    
sniff(filter='tcp src port 6040', prn=process_packet, store=0)
