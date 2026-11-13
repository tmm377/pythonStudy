"""自己写上下文管理器：计时器（类版）

__enter__ 记起点，__exit__ 算差值。计时范围天然覆盖整个 with 块。

比 09_with.py 里那版改了三处：
1. time.time() → time.perf_counter()：墙钟会被系统对时改动，可能出现负数；
   perf_counter 是单调计数器，专门用来测耗时。
2. 加 label：多个计时器同时用时，输出分得清是谁的。
3. 把耗时存到 self.elapsed：事后还能读，不只打印。
"""

import time


class Timer:
    """用法：with Timer("排序") as t: ...  事后可读 t.elapsed"""

    def __init__(self, label=""):
        self.label = label
        self.start = None
        self.elapsed = None

    def __enter__(self):
        self.start = time.perf_counter()
        return self                     # 这个值就是 as 拿到的东西

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        mark = "（异常退出）" if exc_type else ""
        name = self.label or "代码块"
        print(f"  [{name}] {self.elapsed * 1000:.1f} ms {mark}")
        return False                    # False = 不吞异常，照常往外抛


if __name__ == "__main__":
    print("=== 1. 基本用法 ===")
    with Timer("求和"):
        sum(range(3_000_000))

    print()
    print("=== 2. as 拿到的是 __enter__ 的返回值 ===")
    with Timer("看一眼") as t:
        print("  as 后面是:", type(t).__name__)
        sorted(range(100_000), reverse=True)

    print()
    print("=== 3. 嵌套：内层先退出，时间更短 ===")
    with Timer("外层"):
        sum(range(3_000_000))
        with Timer("内层"):
            sum(range(1_000_000))

    print()
    print("=== 4. 块里抛异常，__exit__ 照样执行 ===")
    try:
        with Timer("出错"):
            raise RuntimeError("故意炸")
    except RuntimeError:
        print("  异常照常抛到外面")

    print()
    print("=== 5. 耗时能带出来 ===")
    with Timer("统计") as t:
        sorted(range(200_000), reverse=True)
    print(f"  事后读取 t.elapsed = {t.elapsed * 1000:.1f} ms")
