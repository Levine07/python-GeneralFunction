#! /usr/bin/python3
# -*-coding='utf8'

"""
levine07
2020-06-22
"""


def getparam(source_buff: bytes, bit_count: int, bit_length: int, bit_type: str) -> tuple:
    """
    按bit获取指定长度的值， 返回补零整字节
    :param source_buff: 源字节
    :param bit_count: 获取位置
    :param bit_length: 获取长度
    :param bit_type: 补零位置： 'front' -- 前补零整字节    'back'--后补零整字节
    :return: 返回tuple  （指定值， 指定值占位）
    """

    if bit_length % 8 > 0:
        return_length = bit_length // 8 + 1
    else:
        return_length = bit_length // 8
    ibytes = bytearray(source_buff[(bit_count - 1) // 8: (bit_count + bit_length - 2) // 8 + 1])
    ibytes[0] = ((ibytes[0] << ((bit_count - 1) % 8)) & 0xff) >> ((bit_count - 1) % 8)
    if bit_type == 'front':
        return int.from_bytes(ibytes, 'big') >> (8 - (bit_count + bit_length - 1)) % 8, return_length
    elif bit_type == 'back':
        zero_fill = 8 - (bit_length % 8)
        if zero_fill != 8:
            return (int.from_bytes(ibytes, 'big')) >> (8 - (bit_count + bit_length - 1)) % 8 << zero_fill, return_length
        else:
            return int.from_bytes(ibytes, 'big') >> (8 - (bit_count + bit_length - 1)) % 8, return_length


def copybit(source_buff:bytes, bit_count: int, bit_length: int, target_buff: bytearray, target_count: int) -> int:
    """
    向目的缓冲区内拷贝指定内容
    :param source_buff: 源缓冲区比特位
    :param bit_count: 源位置
    :param bit_length: 取值长度
    :param target_buff: 目的缓冲区比特位
    :param target_count: 目的位置
    :return: 修改后末尾bit位
    """
    source_return_value, source_return_length = getparam(source_buff, bit_count, bit_length, 'back')
    target_zero_fill = (target_count - 1) % 8                    # 目的地址最后一字节内容，有效比特位
    if target_zero_fill == 0:                                    # 目的位置刚好整字节，直接在目的位置后添加即可
        target_buff += source_return_value.to_bytes(source_return_length, 'big')
    elif (bit_length % 8) == 0 or (8 - target_zero_fill) < (bit_length % 8):    # 左移后不涉及删减
        source_return_value <<= (8 - target_zero_fill)
        source_bytes = source_return_value.to_bytes(source_return_length + 1, 'big')
        target_buff[-1] |= source_bytes[0]
        target_buff += source_bytes[1:]
    elif (8 - target_zero_fill) >= (bit_length % 8):           # 拷贝内容左移后，缓冲区末尾出现空字节情况
        source_return_value <<= (8 - target_zero_fill)
        source_bytes = source_return_value.to_bytes(source_return_length + 1, 'big')
        target_buff[-1] |= source_bytes[0]
        target_buff += source_bytes[1:]
    target_count += bit_length
    return target_count


def crc_table(crc_data):
    crc_table = []
    crc = 0
    for i in range(len(crc_data)):
        temp = (crc_data[i] & 0xff) ^ ((crc >> 16) & 0xff)
        crc = crc_table[temp] ^ ((crc << 8) & oxffff00)
    crc = crc & 0xffffff
    return crc.to_bytes(3, byteorder='big')

