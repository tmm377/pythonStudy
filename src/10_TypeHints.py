"""
10 · 类型提示（Type Hints）

一句话先立住：类型提示是「标签」，不是「约束」。
Python 解释器运行时既不检查、也不强制，更不会自动转换类型；
真正会读这些标签的是 mypy / pyright / PyCharm / VS Code 这类静态检查工具，
以及读代码的人。它换来的是：提前发现参数传反、属性名写错，IDE 补全更准。

注意：第 3 节**故意写了类型错误**来演示「运行时不检查」，
静态检查器在那里报警是预期行为，不是代码写坏了。
"""

from typing import Any, get_type_hints

# ---------------------------------------------------------------
# 1. 变量注解
# ---------------------------------------------------------------
# 语法：变量名: 类型 = 值
# 冒号后面那段叫「注解」，等号右边才是真正的赋值。
# 注解不会把值转成该类型，也不会拦住别的值（下面第 3 节会验证）。

name: str = "Agent"
count: int = 42

# 【修复点】原来写的是 dict[str, any]，这里的 any 是内置函数 any()，（用来判断「可迭代对象里有没有真值」），不是类型。
# 这种写法运行时不报错，但语义完全错，mypy / pyright 会报"Function 'any' is not valid as a type"，IDE 也会划红线。
# 正确写法是从 typing 导入首字母大写的 Any，表示「值可以是任意类型」。
config: dict[str, Any] = {"model": "gpt-4"}

# 取舍：若确定所有值都是字符串，写 dict[str, str] 更精确，
# 检查器能帮你查出 config["port"] = 8080 这类笔误；
# 但配置字典常混着 str / int / bool / 嵌套结构，那就只能用 Any，
# 代价是检查器不再检查「值」的类型（键仍然被约束为 str）。
labels: dict[str, str] = {"env": "dev", "mode": "study"}

# 只写注解、不赋值也合法：这一行不会创建 pending 变量，
# 只是在模块的 __annotations__ 里记了一笔（真去访问 pending 会 NameError）。
pending: str

# list[str] / dict[str, Any] 这种「内置类型当泛型，即：类型[类型参数]」的写法需要 Python 3.9+；
# 老代码里的 typing.List[str] / typing.Dict[...] 是同一回事，不必再学。
# str | None 这类联合类型要 3.10+。本项目要求 >= 3.11，都能直接用。


# ---------------------------------------------------------------
# 2. 函数注解
# ---------------------------------------------------------------
# 语法：def 函数(参数: 类型 = 默认值) -> 返回值类型:
# - 箭头 -> 只描述返回值；参数后面只用冒号。
# - 有默认值的参数照常写默认值，注解放在冒号后、等号前。
# - 函数没有返回值时写 -> None（不是留空）。
# - 注解不参与函数体执行，self / cls 通常也不用注解。


def greet(name: str, times: int = 1) -> str:
    """参数和返回值都有注解；函数体跟没写注解时一模一样。"""
    return f"Hello, {name}! " * times


def search_web(query: str, max_results: int = 10) -> list[str]:
    """搜索结果返回字符串列表（list[str] 读作「元素都是 str 的列表」）。"""
    return [f"结果{i}: 关于 {query}" for i in range(max_results)]


# ---------------------------------------------------------------
# 3. 运行时验证：注解到底做了什么
# ---------------------------------------------------------------
if __name__ == "__main__":
    print("=== 1. 正常调用 ===")
    print("  greet:", greet("Agent", 2))
    print("  search:", search_web("AI", 3))

    print("\n=== 2. 注解不检查运行时值（本节故意写错）===")
    wrong: int = "我其实是字符串"
    print(f"  wrong 标注成 int，实际是 {type(wrong).__name__}: {wrong!r}")

    # 注解说 name 是 str，传 int 照样执行 —— f-string 能格式化任何对象。
    print("  greet(123, 2) ->", greet(123, 2))

    # 这里确实会报错，但错的是 * 运算（str 不能乘 str），
    # 不是「类型检查器发现 times 不是 int」：解释器压根没看注解。
    try:
        greet("Agent", "2")
    except TypeError as e:
        print("  greet('Agent', '2') ->", type(e).__name__, ":", e)

    print("\n=== 3. 注解存在哪儿 ===")
    print("  greet.__annotations__ :", greet.__annotations__)
    print("  get_type_hints(greet) :", get_type_hints(greet))
    print("  模块级 __annotations__:", __annotations__)

    print("\n=== 4. 让注解真正起作用 ===")
    print("  解释器不检查，要交给静态工具：")
    print("    .venv/bin/python -m pip install mypy")
    print("    .venv/bin/mypy src/10_TypeHints.py")
    print("  或在 PyCharm / VS Code 里打开类型检查。")


# ---------------------------------------------------------------
# 4. 常见写法速查（只是参考，不执行）
# ---------------------------------------------------------------
# def find(key: str) -> str | None:            # 可能返回 None（3.10+）
# def parse(data: str | bytes) -> int:         # 联合类型
# def batch() -> list[dict[str, Any]]:         # 嵌套容器
# def log(msg: str) -> None:                   # 没有返回值
# from collections.abc import Callable
# def apply(fn: Callable[[int], str]) -> list[str]:   # 回调函数
#
# 进阶一句：文件顶部加 from __future__ import annotations（3.14 起成为默认）
# 会把注解统一存成字符串，用来解决「类型定义在后面 / 互相引用」的前向引用问题；
# 需要真实类型对象时用 get_type_hints() 还原。本文件没加，所以上面打印的是类型对象。
