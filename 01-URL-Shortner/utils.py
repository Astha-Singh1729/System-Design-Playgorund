BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode(num: int) -> str:
    if num == 0:
        return BASE62[0]

    arr = []
    base = len(BASE62)
    while num:
        num, rem = divmod(num, base)
        arr.append(BASE62[rem])
    
    arr.reverse()
    return "".join(arr)

def decode(string: str) -> int:
    base = len(BASE62)
    strlen = len(string)
    num = 0

    for idx, char in enumerate(string):
        power = (strlen - (idx + 1))
        num += BASE62.index(char) * (base ** power)
    
    return num
