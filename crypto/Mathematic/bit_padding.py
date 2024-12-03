LEFT_PADDING_SIZE = 5
RIGHT_PADDING_SIZE = 2
from typing import Callable
class BitPaddingConfig:
    def __init__(self, LEFT_PADDING_SIZE: int, RIGHT_PADDING_SIZE: int):
        self.LEFT_PADDING_SIZE = LEFT_PADDING_SIZE
        self.RIGHT_PADDING_SIZE = RIGHT_PADDING_SIZE
    
    def __repr__(self) -> str:
        return f"BitPaddingConfig(LEFT_PADDING_SIZE={self.LEFT_PADDING_SIZE}, RIGHT_PADDING_SIZE={self.RIGHT_PADDING_SIZE})"

def pad(config: BitPaddingConfig, original_number: int, check_func: Callable[[int], bool]) -> int|None:
    LEFT_PADDING_SIZE = config.LEFT_PADDING_SIZE
    RIGHT_PADDING_SIZE = config.RIGHT_PADDING_SIZE

    K = original_number.bit_length() + (LEFT_PADDING_SIZE - 1) + RIGHT_PADDING_SIZE
    left_pad_base = (1 << (K + 1))
    x = left_pad_base + original_number << RIGHT_PADDING_SIZE
    for left_pad_additional in range(0, 2 ** (LEFT_PADDING_SIZE - 1)):
        for right_pad in range(0, 2 ** RIGHT_PADDING_SIZE):
                candidate = (left_pad_additional << K) + x + right_pad
                if check_func(candidate):
                    return candidate
    return None

def unpad(config: BitPaddingConfig, padded_number: int) -> int:
    LEFT_PADDING_SIZE = config.LEFT_PADDING_SIZE
    RIGHT_PADDING_SIZE = config.RIGHT_PADDING_SIZE

    x = padded_number >> RIGHT_PADDING_SIZE
    x = x & ((1 << (x.bit_length() - LEFT_PADDING_SIZE - 1)) - 1)
    return x