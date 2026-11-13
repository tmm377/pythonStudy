"""__exit__ 的返回值：吞异常还是不吞

    return False / None  →  异常继续往外抛（默认，正确选择）
    return True          →  异常被"处理掉了"，不再上抛（危险）

只有明确要把某种异常转成正常流程时才返回 True。
标准库的 contextlib.suppress(FileNotFoundError) 就是这么实现的。
"""


class Swallow:
    """只吞 ValueError，其他异常照常抛"""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  [__exit__] 收到异常类型 = {exc_type.__name__ if exc_type else None}")
        if exc_type is ValueError:
            print("  [__exit__] 是 ValueError，吞掉")
            return True
        return False


class Pass:
    """什么都不管，永远返回 False"""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  [__exit__] 收到异常类型 = {exc_type.__name__ if exc_type else None}")
        return False


if __name__ == "__main__":
    print("=== 1. 正常退出：三个参数都是 None ===")
    with Pass():
        pass

    print()
    print("=== 2. 返回 False：异常继续抛 ===")
    try:
        with Pass():
            raise ValueError("会传出去")
    except ValueError as e:
        print("  上层收到:", e)

    print()
    print("=== 3. 返回 True：异常被吞掉 ===")
    with Swallow():
        raise ValueError("这条不会传出去")
    print("  程序继续往下走了 —— 说明异常真的消失了")

    print()
    print("=== 4. 只吞指定的类型，其他照样抛 ===")
    try:
        with Swallow():
            raise TypeError("这个我不吞")
    except TypeError as e:
        print("  上层收到:", e)

    print()
    print("=== 5. 标准库里的同类工具 ===")
    import contextlib
    with contextlib.suppress(FileNotFoundError):
        open("/tmp/这个文件不存在.txt")
    print("  suppress(FileNotFoundError) 之后没崩，继续执行")
