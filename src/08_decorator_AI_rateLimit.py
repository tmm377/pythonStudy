"""场景 2：限流保护 —— @rate_limit(每秒最多几次)

思路：记住"上一次调用结束的时间"，下次调用前算一下间隔够不够，
不够就 sleep 补齐。间隔由参数换算：interval = 1 / max_calls_per_second。

两个设计细节值得注意：
1. last_called 用**列表** [0] 而不是普通变量 —— 因为要跨次调用保存状态，
   用列表可以原地修改；用普通变量就得写 nonlocal。
2. 时间戳记在**函数执行完之后**，所以真正的间隔是
   「函数耗时 + sleep 补齐」= 至少 interval。
"""

import time
from functools import wraps


def rate_limit(max_calls_per_second):
    """第一层：算出最小间隔"""
    interval = 1.0 / max_calls_per_second
    last_called = [0.0]              # 闭包状态：用列表才能原地改

    def decorator(func):
        """第二层：接住被装饰的函数"""
        @wraps(func)                 # 保留原函数的名字/文档/签名
        def wrapper(*args, **kwargs):
            """第三层：每次调用前检查是否需要等待"""
            elapsed = time.time() - last_called[0]
            if elapsed < interval:
                time.sleep(interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()     # 记录本次结束时间
            return result
        return wrapper
    return decorator


# ============ 演示用：假装在调一个外部 API ============
@rate_limit(4)                       # 每秒最多 4 次
def call_api(n):
    """调一次外部接口，返回响应文本。"""  # call_api.__doc__拿到的就是这个文案
    time.sleep(0.05)                 # 模拟网络耗时 50ms
    return f"响应#{n}"


def call_api_unlimited(n):
    """对照组：不加限流"""
    time.sleep(0.05)
    return f"响应#{n}"


if __name__ == "__main__":
    print("=== 1. 不加限流：6 次调用几乎瞬间打完 ===")
    t0 = time.perf_counter()
    for i in range(1, 7):
        call_api_unlimited(i)
    cost = time.perf_counter() - t0
    print(f"  总耗时 {cost:.2f}s  →  约 {6 / cost:.1f} 次/秒")

    print()
    print("=== 2. @rate_limit(4)：被压到每秒 4 次 ===")
    t0 = time.perf_counter()
    prev = None
    for i in range(1, 7):
        call_api(i)
        now = time.perf_counter()
        gap = f"{now - prev:.2f}s" if prev else "—"
        last_called_at = f"{now - t0:.2f}s"
        print(f"  第 {i} 次  时间轴 {last_called_at:>5}   距上次 {gap}")
        prev = now
    cost = time.perf_counter() - t0
    print(f"  总耗时 {cost:.2f}s  →  约 {6 / cost:.1f} 次/秒")

    print()
    print("=== 3. 算一下理论值 ===")
    print("  interval = 1/4 = 0.25s，每次先等 0.25s 再花 0.05s 执行")
    print("  每次的实际周期 ≈ 0.25 + 0.05 = 0.31s")
    print("  6 次 ≈ 首次 0.05 + 5 × 0.31 = 1.60s")
    print("  ↑ 注意：不是 4 次/秒，是 ≈ 3.7 次/秒")
    print("    因为计时点记在函数执行之后，函数自己的耗时被算进了间隔里")

    print()
    print("=== 4. 装饰器的元信息还在（@wraps 的作用）===")
    print("  名字:", call_api.__name__)
    print("  文档:", call_api.__doc__ or "（无）")
