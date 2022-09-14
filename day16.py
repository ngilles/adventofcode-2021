
import dataclasses
from re import sub
from typing import Generator, Iterator, Tuple, TypeVar, List
from dataclasses import dataclass
from parsy import digit, char_from, string, string_from
from functools import reduce
from operator import add, mul, gt, lt, eq

T = TypeVar('T')

_bits = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

def intify(s: str):
    return sum(2**idx for idx, c in enumerate(reversed(s)) if c == '1')

# bit = char_from('01')
# bits = bit.many().map(intify)


def take(it: Iterator[T], n: int) -> Tuple[T,...]:
    elems = []
    while n > 0:
        elems.append(next(it))

    return tuple(elems)

def bitify(s: str) -> Generator[int, None, None]:
    for c in s:
        yield from _bits[c]

example = 'D2FE28'

ops = {
    0: add,
    1: mul,
    2: min,
    3: max,
    5: gt,
    6: lt,
    7: eq,
}

@dataclass
class Packet:
    packet_version: int
    type_id: int

    def get_version_sum(self):
        return self.packet_version

@dataclass
class LiteralPacket(Packet):
    value: int

    def get_value(self):
        return self.value

@dataclass
class OperatorPacket(Packet):
    packets: List[Packet]

    def get_version_sum(self):
        return self.packet_version + sum(packet.get_version_sum() for packet in self.packets)

    def get_value(self):
        return reduce(ops[self.type_id], (packet.get_value() for packet in self.packets))


def parse_packet(s: str, pos: int):
    packet_version = intify(s[pos:pos+3])
    type_id = intify(s[pos+3: pos+6])

    if type_id == 4:
        return parse_literal_packet(s, pos)
    else:
        return parse_operator_packet(s, pos)


def parse_literal_packet(s: str, pos: int):
    packet_version = intify(s[pos:pos + 3])
    type_id = intify(s[pos+3:pos+6])
    value, pos = parse_int(s, pos+6)

    return LiteralPacket(packet_version, type_id, value), pos


def parse_operator_packet(s: str, pos: int):
    packet_version, pos = read_int(s, 3, pos)
    type_id, pos = read_int(s, 3, pos)
    length_type_id = s[pos]
    pos += 1
    packets = []

    if length_type_id == '0':
        length, pos = read_int(s, 15, pos)
        start = pos
        print(f'operator packet with size: {length}')
        while pos - start < length:
            packet, pos = parse_packet(s, pos)
            packets.append(packet)
    else:
        sub_packets, pos = read_int(s, 11, pos)
        print(f'operator packet with sub packets: {sub_packets}')
        while sub_packets:
            packet, pos = parse_packet(s, pos)
            packets.append(packet)
            sub_packets -= 1

    return OperatorPacket(packet_version, type_id, packets), pos


def read_int(s: str, n: int, pos: int):
    value = intify(s[pos:pos+n])
    return value, pos + n


def parse_int(s: str, pos: int):
    bits = []
    while s[pos] == '1':
        bits.extend(s[pos + 1:pos + 5])
        pos += 5
    bits.extend(s[pos+1:pos+5])
    pos += 5

    return intify(bits), pos

#bits = ''.join(bitify('D2FE28'))
bits = ''.join(bitify('38006F45291200'))
#bits = ''.join(bitify('EE00D40C823060'))
bits = ''.join(bitify('8A004A801A8002F478')) # 16
bits = ''.join(bitify('620080001611562C8802118E34')) # 12
#bits = ''.join(bitify('C0015000016115A2E0802F182340')) # 23
#bits = ''.join(bitify('A0016C880162017C3686B18A3D4780')) # 31
bits = ''.join(bitify('C200B40A82')) # 3
bits = ''.join(bitify('04005AC33890')) # 54
bits = ''.join(bitify('880086C3E88112')) # 7
bits = ''.join(bitify('CE00C43D881120')) # 9
bits = ''.join(bitify('D8005AC2A8F0')) # 1
bits = ''.join(bitify('F600BC2D8F')) # 0
bits = ''.join(bitify('9C005AC2F8F0')) # 0
bits = ''.join(bitify('9C0141080250320F1802104A08')) # 1
bits = ''.join(bitify(open('inputs/day-16-input.txt').read()))

packet, pos = parse_packet(bits, 0)

print(packet)
print(packet.get_version_sum())
print(packet.get_value())