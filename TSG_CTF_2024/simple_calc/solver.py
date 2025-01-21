import itertools
import multiprocessing
import os
from tqdm import tqdm 
from unicodedata import numeric

# --- server.pyから引用 ---
def calc(s):
    if (loc := s.find('+')) != -1:
        return calc(s[:loc]) + calc(s[loc+1:])
    if (loc := s.find('*')) != -1:
        return calc(s[:loc]) * calc(s[loc+1:])
    x = 0
    for c in s: x = 10 * x + numeric(c)
    return x
# --- 引用ここまで ---
 
CHARS = {"+": "+", "*": "*"}
for code_point in range(0x110000):
    char = chr(code_point)
    if char.isnumeric():
        CHARS[numeric(char)] = char  # 同じ数字を表す場合は除外
CHARS = CHARS.values()
MIN = 12345678
MAX = MIN + 40

def generate_expressions():
    for expr in itertools.product(CHARS, repeat=5):
        yield ''.join(expr)

def chunkify(iterable, chunk_size):
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    if chunk:  # 残った要素があれば
        yield chunk

def process_expressions_chunk(expr_chunk):
    results = {}
    for expr in expr_chunk:
        result = int(calc(expr))
        if MIN <= result < MAX:
            results[result] = expr
    return results

if __name__ == '__main__':
    valid_expressions = {}

    with multiprocessing.Pool(processes=os.cpu_count()) as pool:        
        chunk_size = 10000

        for result in tqdm(
            pool.imap(process_expressions_chunk, chunkify(generate_expressions(), chunk_size)),
            total=len(CHARS) ** 5 // chunk_size
        ):
            valid_expressions.update(result)
            if len(valid_expressions) == MAX - MIN:
                break

    for key, value in sorted(valid_expressions.items()):
        print(f"{key}: {value.encode()}")
