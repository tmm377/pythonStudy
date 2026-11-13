"""with 的实用模式：事务 + 多个资源

事务的关键是 __exit__ 里不能吞异常：
    成功 → COMMIT
    失败 → ROLLBACK，然后把异常 raise 回去

回滚是善后，不是免责。调用方仍然需要知道出事了。
"""

from contextlib import contextmanager


@contextmanager
def transaction(name):
    print(f"  BEGIN   {name}")
    try:
        yield
        print(f"  COMMIT  {name}")
    except Exception as e:
        print(f"  ROLLBACK {name}  （原因: {e}）")
        raise                           # 交回去，不吞


class Res:
    """模拟需要成对打开/关闭的资源，比如文件、连接、锁"""

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"  打开 {self.name}")
        return self

    def __exit__(self, *exc):
        print(f"  关闭 {self.name}")
        return False


if __name__ == "__main__":
    print("=== 1. 事务：成功提交 ===")
    with transaction("转账"):
        print("  扣款成功")

    print()
    print("=== 2. 事务：失败回滚，异常继续上抛 ===")
    try:
        with transaction("转账"):
            print("  扣款成功")
            raise RuntimeError("余额不足")
    except RuntimeError:
        print("  上层收到异常，事务已回滚")

    print()
    print("=== 3. 多个资源：关闭顺序后进先出 ===")
    with Res("A") as a, Res("B") as b:
        print("  使用 A 和 B")
    print("  ↑ B 先关，因为 B 可能是基于 A 打开的")

    print()
    print("=== 4. 资源多了可以换行（Python 3.10+）===")
    with (
        Res("连接"),
        Res("游标"),
    ):
        print("  执行查询")
