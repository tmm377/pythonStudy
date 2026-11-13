"""
10 · 组合类型（Composite Types）

把基本类型拼起来描述更复杂的数据：
    可空 T | None、多选 str | bytes、
    容器 list[str] / dict[str, float] / tuple[float, float]。

前提回顾（见 10_TypeHints.py）：类型提示只是标签，运行时不检查，
真正检查的是 mypy / pyright / IDE。本项目要求 Python >= 3.11，
所以统一使用 3.10+ 的 `|` 写法，旧写法留作「读旧代码时认得」。

注意：第 4 节演示里**故意传了不符合注解的值**（process(123)），
静态检查器在那里报警是预期行为，不是代码写坏了。
"""

from typing import get_type_hints

# ------------------------------------------------------------------
# 1. 可空类型：T | None
# ------------------------------------------------------------------
# 【改写点】原来写的是 Optional[str]（从 typing 导入），那是 3.10 之前的写法。
# 现在写 str | None，读作「str 或者 None」。
# 两者语义等价，在 3.10+ 里 Optional[str] == (str | None) 结果也是 True；
# 但底层对象不同（typing 的 Union 别名 vs types.UnionType），第 4 节会打印验证。
# 老写法什么时候还会见到：旧项目、老教程、或必须兼容 3.9 及以下的库。
#
# 典型来源：dict.get(key) 找不到时返回 None，所以返回值天然是 str | None。
# 参数原名叫 id，会遮蔽内置函数 id()（取对象身份）；按惯例改名 user_id。


def get_user(user_id: int) -> str | None:
    """按 id 查名字，查不到返回 None。"""
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)


# ------------------------------------------------------------------
# 2. 联合类型：A | B
# ------------------------------------------------------------------
# 【改写点】原来写的是 Union[str, bytes]，同样换成 3.10+ 的 str | bytes。
# 这里的 isinstance 有个专门名字：类型收窄（type narrowing）。
# 静态检查器看到 if isinstance(data, bytes)，就知道这个分支里 data 是 bytes，
# 可以放心调 .decode()；另一个分支则推断为 str，直接 return 符合 -> str。
# 这是注解与运行时代码配合得最紧密的地方。
#
# 但注解不负责校验输入：真传个 int 进来，会走到 return data 原样返回 int，
# 运行时照样不报错（只是骗过了类型声明）。要严格就得自己加 else: raise TypeError。


def process(data: str | bytes) -> str:
    """接受 str 或 bytes，统一返回解码后的 str。"""
    if isinstance(data, bytes):
        return data.decode("utf-8")
    return data


# ------------------------------------------------------------------
# 3. 容器类型：list / dict / tuple
# ------------------------------------------------------------------
# 【清理点】原文件 import 了 List, Dict, Tuple, Optional, Union，
# 其中 List / Dict / Tuple 一个都没用到 —— 它们是 3.9 之前的旧式泛型
# （typing.List[str] 等），3.9+ 直接用内置类型的下标写法，不必从 typing 导入。
# 现已删掉未使用的导入，Optional / Union 也换成了 `|`。

tools: list[str] = ["search", "read_file"]
#   ↑ 读作「元素都是 str 的列表」，不限长度。
#   对比 list[Any]（什么都能放）、list[str | int]（元素可以是两种）。

config: dict[str, float] = {"temperature": 0.7, "top_p": 0.9}
#   ↑ dict 有两个参数：第一个是「键」的类型，第二个是「值」的类型。
#   若值可能混着 str / int / bool，得写 dict[str, Any]（Any 从 typing 导入），
#   代价是检查器不再管值的类型 —— 10_TypeHints.py 里讲过这个取舍。

coord: tuple[float, float] = (116.40, 39.90)
#   ↑ tuple 的下标写法有两种，别混：
#       tuple[float, float]  固定 2 个元素，第 1 个 float、第 2 个 float
#       tuple[float, ...]    任意长度，但每个元素都是 float（... 是省略号字面量）
#   list[str] 只管「元素是什么」不管长度；tuple[...] 能精确到「每个位置」。
#   顺带一提，这两个值是北京的 (经度, 纬度)，两个位置都是 float，类型一致。


# ------------------------------------------------------------------
# 4. 运行时验证
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("=== 1. 可空类型 ===")
    print("  get_user(1) ->", get_user(1))
    print("  get_user(9) ->", get_user(9), "| 实际类型:", type(get_user(9)).__name__)
    # 拿到 str | None 之后，调用方必须先判断再使用，不能直接 .upper()：
    # 静态检查器会拦住 found.upper()，因为它可能是 None。
    found = get_user(1)
    if found is not None:
        print("  非空分支里可以放心用 .upper():", found.upper())

    print("\n=== 2. 联合类型 ===")
    print("  process('中文') ->", process("中文"))
    print("  process(b'hi')  ->", process(b"hi"))
    print("  注解不校验输入，传 int 照样返回:", repr(process(123)))

    print("\n=== 3. 注解存在哪儿 ===")
    print("  模块级 __annotations__:")
    for key, value in __annotations__.items():
        print(f"    {key}: {value}")
    print("  get_type_hints(get_user):", get_type_hints(get_user))

    print("\n=== 4. 新旧写法对照 ===")
    # 这里只为对照临时导入，实际写新代码不需要它们。
    from typing import Optional, Union
    print("  Optional[str]          :", Optional[str])
    print("  str | None             :", str | None)
    print("  两者相等吗             :", Optional[str] == (str | None))
    print("  Union[str, bytes] == str | bytes:", Union[str, bytes] == (str | bytes))


# ------------------------------------------------------------------
# 5. 常见组合写法速查（只是参考，不执行）
# ------------------------------------------------------------------
# list[dict[str, Any]]            一批配置字典
# dict[str, list[str]]            键到字符串列表的映射
# tuple[str, int, bool]           定长、每位类型可以不同（比 dataclass 轻）
# str | int | None                三种可能，`|` 可以连写
# Callable[[str, int], bool]     函数类型：参数是 (str, int)，返回 bool
# Literal["asc", "desc"]         只能是这几个字面值（from typing import Literal）
# TypedDict                      给 dict 每个键单独指定类型，比 dict[str, Any] 精确
#
# 判断口诀：容器看「里面装什么」，联合看「可能是哪几种」，
# Optional 只解决「也可能是 None」这一种情况。
