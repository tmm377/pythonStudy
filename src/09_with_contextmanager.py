"""用生成器写上下文管理器：@contextmanager

类版要写 __enter__ / __exit__ 两个方法；生成器版只写一个函数，两种写法是同一个套协议的两种写法：

    yield 之前的内容  →  __enter__（进入时执行）
    yield 的值        →  as 拿到的东西
    yield 之后的内容  →  __exit__（退出时执行）

必须用 try/finally 包住 yield，否则异常时后半段直接不执行，清理被静默跳过。
"""

import time
from contextlib import contextmanager


# ---------- 写法一：类（12 行）直接实现__enter__/__exit__ ----------
class TimerClass:
    def __init__(self, label=""):
        self.label = label

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *exc):
        cost = (time.perf_counter() - self.start) * 1000
        print(f"  [类版 {self.label}] {cost:.1f} ms")
        return False


# ---------- 写法二：生成器（8 行）生成器函数+@contextmanager ----------
@contextmanager
# @contextmanager 的生成器必须恰好 yield 一次。零次会在 __enter__ 报 generator didn't yield，两次会在 __exit__ 报 generator didn't stop。这是生成器版唯一比类版脆弱的地方
def timer_gen(label=""):
    start = time.perf_counter()
    try:
        # 异常从 yield 处被 throw 进来、不捕获、原样冒出，让 @contextmanager 判定「未抑制」
        yield label.upper()             # 这里的值就是 as 拿到的
    finally:
        print(f"  [生成器版 {label}] {(time.perf_counter() - start) * 1000:.1f} ms")


# ---------- 反例：忘了 try/finally ----------
@contextmanager
def bad_timer(label=""):
    start = time.perf_counter()
    yield
    print(f"  [坏的 {label}] 这句在异常时不会执行")


if __name__ == "__main__":
    print("=== 1. 两种写法效果一样 ===")
    with TimerClass("A"):
        sum(range(1_000_000))
    with timer_gen("A"):
        sum(range(1_000_000))

    print()
    print("=== 2. as 拿到的值来自 yield ===")
    with timer_gen("计算") as name:
        print("  as 拿到:", name)

    print()
    print("=== 3. 异常时生成器版也会走 finally ===")
    try:
        with timer_gen("出错"):
            raise RuntimeError("故意炸")
    except RuntimeError:
        print("  异常传到外面了")

    print()
    print("=== 4. 反例：忘了 try/finally，异常时清理被跳过 ===")
    try:
        with bad_timer("出错"):
            raise RuntimeError("炸")
    except RuntimeError:
        print("  注意上面没有打印「这句在异常时不会执行」")
        print("  ↑ 这就是为什么 yield 必须包在 try/finally 里")
