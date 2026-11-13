"""用 contextlib.contextmanager 快速创建上下文管理器

场景：临时修改一个环境变量，离开 with 时无论成功还是抛异常都还原。

@contextmanager 会把「生成器函数」包装成带 __enter__ / __exit__ 的对象：
    yield 之前  → __enter__（进入时执行）
    yield 那行  → 暂停，with 块里的代码在这期间运行
    yield 之后  → __exit__（退出时执行）

提醒：os.environ 是进程级全局状态，多线程 / 异步里改它并不安全。
"""

import os
from contextlib import contextmanager

DEMO_KEY = "DEMO_API_KEY"


@contextmanager
def temporary_env_var(key, value):
    """临时把 os.environ[key] 设为 value，退出时恢复原状。

    key   : 环境变量名
    value : 临时值，os.environ 只接受字符串
    """
    # os.environ 的值只能是 str，传别的类型会在赋值时 TypeError，这里先拦住
    if not isinstance(value, str):
        raise TypeError("环境变量的值必须是 str")

    # 先存旧值。变量不存在时 get 返回 None；
    # 而环境变量的值永远是字符串、不可能是 None，
    # 所以 None 可以安全地当作「原本不存在」的标记。
    old_value = os.environ.get(key)

    os.environ[key] = value              # yield 之前 = __enter__：改状态

    try:
        # 函数在这里暂停，让 with 块执行；光秃秃的 yield 不交出值，
        # 所以 `as x` 会拿到 None（写成 `yield value`，as 就能拿到临时值）。
        # 块内若抛异常，@contextmanager 会用 gen.throw() 把异常扔回这一行：
        # 下面的 finally 照样执行，异常再原样冒出去（等价于 return False）。
        yield
    finally:
        # yield 之后 = __exit__：无条件还原，异常路径也不会漏。
        if old_value is None:
            # 原本没有这个变量 → 退出时删掉。
            # 用 pop(key, None) 而不是 del：万一 with 块内自己删了它，
            # del 会抛 KeyError，反而把收尾搞坏、盖住原始异常。
            os.environ.pop(key, None)
        else:
            os.environ[key] = old_value


def call_api():
    """占位函数：真实项目里这里会去调用接口。"""
    print("  call_api() 读到:", os.environ.get(DEMO_KEY))


if __name__ == "__main__":
    # 用 DEMO_API_KEY 而不是真实的 OPENAI_API_KEY：
    # 既避免误改 / 打印真实密钥，也方便看清「设置 → 还原」的过程。
    os.environ.pop(DEMO_KEY, None)       # 清场，保证演示从「变量不存在」开始

    print("=== 1. 原本不存在：进入时设置，退出后删除 ===")
    print("  进入前:", os.environ.get(DEMO_KEY))
    with temporary_env_var(DEMO_KEY, "sk-test"):
        call_api()
    print("  退出后:", os.environ.get(DEMO_KEY))

    print()
    print("=== 2. 原本有值：退出后恢复旧值，而不是删掉 ===")
    os.environ[DEMO_KEY] = "original"
    with temporary_env_var(DEMO_KEY, "sk-test"):
        call_api()
    print("  退出后:", os.environ.get(DEMO_KEY))
    os.environ.pop(DEMO_KEY, None)

    print()
    print("=== 3. 块内抛异常：finally 依然还原，异常照样传出 ===")
    try:
        with temporary_env_var(DEMO_KEY, "sk-test"):
            raise RuntimeError("故意炸")
    except RuntimeError:
        print("  异常传到外面了")
    print("  退出后:", os.environ.get(DEMO_KEY))

    print()
    print("=== 4. 块内自己删掉变量：pop 保证收尾不报 KeyError ===")
    with temporary_env_var(DEMO_KEY, "sk-test"):
        del os.environ[DEMO_KEY]
    print("  正常收尾，没有 KeyError")
