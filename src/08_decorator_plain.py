"""例三：不带参数的装饰器 —— 只有两层

对照用。看它跟 08_decorator_repeat.py 差在哪：
    repeat(3)  -> decorator -> wrapper     三层，因为要先吃一个参数
    simple_log ->             wrapper     两层，直接吃函数

@simple_log 没有括号，因为它本身就是装饰器，不是"生产装饰器的工厂"。
"""

from functools import wraps


def simple_log(func):
    """第一层就是最后一层：直接接收函数"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  [log] 调用 {func.__name__}{args}")
        return func(*args, **kwargs)
    return wrapper


@simple_log
def add(a, b):
    return a + b


if __name__ == "__main__":
    print("=== @simple_log 不带参数 ===")
    print("  返回值:", add(1, 2))

    print()
    print("=== 证明 @wraps 干了活 ===")
    print("  函数名还是:", add.__name__)
    print("  文档还是  :", add.__doc__)

    print()
    print("=== 加个括号会怎样（这是常见误用） ===")
    try:
        @simple_log()
        def broken():
            return 1
    except TypeError as e:
        print("  TypeError:", e)
        print("  ↑ simple_log() 先执行了，但需要 func，所以缺一个参数")
