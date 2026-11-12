"""例二：带默认值参数的装饰器 —— @timer(precision=1)

跟 @repeat(3) 结构完全一样，只是第一层多了默认值。
默认值让装饰器可以这样用：
    @timer                  # 全用默认
    @timer()                # 显式空参
    @timer(precision=1)     # 只改想改的那个
    @timer(3, "s")          # 全按位置

注意：要支持 @timer 这种"不带括号"的写法，需要额外判断 func 是不是函数，
      这里只做 @timer(...) 带括号的形式，保持三层结构干净。
"""

from functools import wraps
import time


def timer(precision=2, unit="ms"):
    """第一层：precision 几位小数，unit 单位（ms / s）"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            cost = time.perf_counter() - start
            if unit == "ms":
                cost *= 1000
            print(f"  [{func.__name__}] 耗时 {cost:.{precision}f} {unit}")
            return result
        return wrapper
    return decorator


@timer(precision=1)
def sum_of_squares(n):
    return sum(i * i for i in range(n))


@timer(precision=3, unit="s")
def tiny_job():
    return sum(range(10_000))


if __name__ == "__main__":
    print("=== @timer(precision=1) 用默认单位 ms ===")
    total = sum_of_squares(1_000_000)
    print("  结果:", total)

    print()
    print("=== @timer(precision=3, unit='s') 两个参数都换掉 ===")
    print("  结果:", tiny_job())
