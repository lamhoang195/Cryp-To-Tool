import sys

# Thiết lập giới hạn lớn cho chuỗi chuyển thành số nguyên
sys.set_int_max_str_digits(2147483647)  # Tăng giới hạn lên tối đa 2^31 - 1

# Hàm tính b^n mod m với n có thể là số rất lớn
def modpower(b: int, n: int, m: int) -> int:
    x = 1
    b %= m
    while n != 0:
        if n % 2 == 1:  # Nếu n là số lẻ
            x = (x * b) % m
        b = (b * b) % m  # Tính bình phương b
        n //= 2  # Chia n cho 2
    return x

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        b = int(sys.argv[1])  # Cơ sở b
        n = int(sys.argv[2])  # Lũy thừa n (có thể là số rất lớn)
        m = int(sys.argv[3])  # Mô-đun m
        result = modpower(b, n, m)
        print(f"b ^ n mod m = {result}")
