# ==================================================================
# 10 · 进阶类型标注：TypedDict / Literal / Callable / 自引用
#
# 这份文件只做「形状声明」：描述字典该有哪些键、值能取哪几个、
# 函数该长什么样。全文没有任何调用，所以直接运行不会有任何输出。
# 关键前提：类型提示不做运行时检查，真正读它的是 mypy / pyright / IDE。
#
# 阅读主线：
#   TypedDict   → 给「字典」定形状（有哪些键、各是什么类型）
#   Literal     → 把值限定成几个具体的字面量
#   Callable    → 给「函数 / 可调用对象」标类型
#   "TreeNode"  → 类还没定义完时，怎么先引用自己
# ==================================================================

from typing import TypedDict, Literal, Callable

# 这三个必须从 typing 导入：它们不是内置类型，而是「类型构造工具」。
#   TypedDict  描述有固定键的字典
#   Literal    描述「只能是这几个值」
#   Callable   描述可调用对象的参数与返回值
# 对比上一节：list[str] / dict[str, float] 用的是内置类型，写下标就行，
# 不用 import；而「字典的形状」「字面量取值」「函数签名」这三件事，
# 内置类型表达不了，才需要 typing 提供专门工具。

# TypedDict — 定义字典的"形状"
# 【它是什么】TypedDict 声明的是「一个 dict 应该有哪些键、每个键的值是什么类型」，
# 不是定义一个有方法的类。ToolResult 看着像类，但运行时：
#     r = ToolResult(tool_name="search", status="success", output="ok", duration_ms=1.5)
#     type(r) 是 dict，不是 ToolResult；只能用 r["status"]，不能写 r.status。
# 我实测过：ToolResult 本身是 _TypedDictMeta，构造出来的确实是普通 dict。
# 【为什么需要它】dict[str, Any] 只说「键是字符串」，检查器不知道里面
# 有没有 duration_ms，键名拼错也发现不了；TypedDict 让检查器能查：
#     r["statuss"]              → 报错：没有这个键
#     r["duration_ms"] = "慢"   → 报错：类型应是 float
# 【注意】这只是标注，运行时照样能塞错值：
#     ToolResult(..., status="unknown", ...) 完全能构造成功（我验证过）。
# TypedDict 不做校验、不能用于 isinstance，它只是给检查器的说明书。
class ToolResult(TypedDict):
    # 类体里只有「键名: 值类型」，没有方法、没有赋值、没有 __init__。
    # 这几行不是类属性定义，而是「键的类型声明」，最终存进 __annotations__。
    tool_name: str
    # Literal["success", "error"] 读作「值只能是字符串 "success" 或 "error"」。
    # 比 str 严格得多：拼错、大小写不对、传别的字符串，静态检查器都会抓到。
    # 但解释器不看它 —— 上面说的 status="unknown" 就是证据。
    status: Literal["success", "error"]   # 只能是这两个值之一
    output: str
    duration_ms: float
    # 对比 dict[str, float]：那里所有值必须同为 float；
    # 这里每个键可以有自己的类型（str / Literal / float 混着来），
    # 这正是 TypedDict 比普通 dict 注解精细的地方。
    # 想让某些键可选，可用 total=False 或 NotRequired（3.11+）。

# Callable — 标注函数类型
# 【读法】Callable[[参数1类型, 参数2类型, ...], 返回值类型]
#   两个逗号层级别看错：方括号里是「参数类型列表」，逗号后面是「返回值类型」。
#   行尾那句 (参数类型) -> 返回类型 是意图说明，不是 Python 的写法。
# 【这一行】ToolHandler 是个「类型别名」（type alias），不是函数也不是类：
#   它代表「接受 (str, dict) 两个参数、返回 ToolResult 形状字典的可调用对象」。
#   起个别名是为了复用；也可以直接写在参数上，效果一样。
# 【精度提醒】这里写的是裸 dict，等价于 dict[Any, Any]（键值都不限）。
#   更精确应写 dict[str, Any]；此处保留原写法，不影响运行，
#   只是静态检查器少了一层约束。
ToolHandler = Callable[[str, dict], ToolResult]  # (参数类型) -> 返回类型

# 【handler 去哪了】这个函数是占位演示：函数体只打印 name，
# 既没把 handler 存起来，也没调用它。真实项目里通常会写
#     handlers[name] = handler
# 之后按名字取出再执行，所以参数类型标注在这里才有意义。
# 【-> None】表示「不返回有意义的值」；省略的话检查器会当成返回 Any。
# 注意 None 不是说「没有返回值」—— Python 函数总会隐式返回 None。
def register_tool(name: str, handler: ToolHandler) -> None:
    """注册一个工具处理器"""
    print(f"已注册工具：{name}")

# 自引用类型（用字符串延迟求值）
# 【为什么必须加引号】__init__ 在 class TreeNode 创建完成之前就开始定义注解了，
# 那一刻名字 TreeNode 还不存在。直接写 left: TreeNode 会立刻 NameError
# （我验证过：name 'X' is not defined）。
# 写成字符串 "TreeNode" 后，Python 只把它当一段文本存进 __annotations__，
# 不求值；mypy / pyright / get_type_hints() 会自己把名字解析出来。
# 实测：__init__.__annotations__ 里是字符串 'TreeNode'，
# 而 get_type_hints(__init__) 还原成了真正的 <class 'TreeNode'>。
# 【另一种解法】文件顶部加 from __future__ import annotations（3.14 起为默认），
# 所有注解统一变成字符串，就可以直接写 TreeNode，这叫「前向引用」。
# 【这行标注的瑕疵】默认值是 None，但注解只写了 "TreeNode"、没包含 None，
# 检查器会报「默认值与注解不匹配」；更准确应写 "TreeNode | None"
# 或 Optional["TreeNode"]。__init__ 也建议补 -> None。
# 两处都只影响静态检查的准确度，不影响运行，这里保留原写法作对照。
class TreeNode:
    def __init__(self, value: int, left: "TreeNode" = None, right: "TreeNode" = None):
        # 下面三行是普通的「实例属性赋值」，跟类型注解无关：
        # 注解只描述「该传什么进来」，是这三行赋值把值真的挂到 self 上。
        # 参数注解不会自动创建 self.value，少写一行就真的没有这个属性。
        self.value = value
        self.left = left
        self.right = right
        # left / right 又指向 TreeNode，于是形成树 / 链表的递归结构；
        # 叶子节点的左右为 None —— 这正是上面注解本该带上 None 的现实原因。

# ==================================================================
# 调用演示：前面的「形状声明」终于被真正用起来。
# 标注本身仍不改运行时行为，真正检查它们的是静态工具：
#   get_type_hints(ToolResult)          → 四个键各自的类型，含 Literal
#   ToolResult.__annotations__          → 同样内容（若用了 future 会是字符串）
#   get_type_hints(TreeNode.__init__)   → 把 'TreeNode' 还原成真正的类
#   mypy 本文件                        → 会指出 left/right 的 None 不匹配
#
# 一句话串起来：TypedDict 管「字典有哪些键」，Literal 管「值能取哪几个」，
# Callable 管「函数长什么样」，字符串注解管「还没定义完就先引用自己」。
# 四者全是描述，不改一行运行时行为 —— 这正是类型提示的基本前提。
# ==================================================================

# 说明：为了不改文件顶部的 import 行，get_type_hints 在演示内部局部导入。
# 上面所有定义（含上一轮加的注释）保持原样，只在下面追加调用代码。

if __name__ == "__main__":
    from typing import get_type_hints

    print("=== 1. ToolResult 造出来其实是普通 dict ===")
    result: ToolResult = ToolResult(
        tool_name="search",
        status="success",
        output="找到 3 条结果",
        duration_ms=12.5,
    )
    print("  type(result) =", type(result).__name__)
    print("  内容 =", result)
    print("  按键取值 result['status'] =", result["status"])

    # 【故意写错】Literal 只允许 "success" / "error"，但运行时没人拦：
    # 静态检查器会在这一行报错，属预期行为，不是代码坏掉了。
    bad: ToolResult = ToolResult(
        tool_name="search", status="unknown", output="", duration_ms=0.0
    )
    print("  故意塞非法 status ->", bad["status"], "（运行时照样成功）")

    print("\n=== 2. 造一个符合 ToolHandler 签名的函数并调用 ===")
    def search(query: str, options: dict) -> ToolResult:
        """search函数的签名是 (str, dict) -> ToolResult，正好匹配 ToolHandler。"""
        return ToolResult(
            tool_name="search",
            status="success",
            output=f"关于 {query} 的结果，limit={options.get('limit', 10)}",
            duration_ms=8.25,
        )

    handler: ToolHandler = search
    # 把函数赋给「类型别名」变量：静态检查器会核对签名是否匹配，
    # 运行时这只是普通赋值，不做任何检查。
    result2: ToolResult = handler("AI Agent", {"limit": 3})
    print("  handler 返回的 type =", type(result2).__name__)
    print("  handler 返回的内容 =", result2)

    print("\n=== 3. 注册工具 ===")
    register_tool("search", handler)
    # 注意：register_tool 的函数体只打印 name，handler 传进去并没被保存或调用。
    # 真实项目里它应该写 handlers[name] = handler；为保持原定义不变，
    # 这里自己建一个注册表，演示「存起来 → 按名字取出 → 再调用」这条链路。
    handlers: dict[str, ToolHandler] = {}
    handlers["search"] = handler
    print("  从注册表取出再调 ->", handlers["search"]("Agent", {})["output"])

    print("\n=== 4. 自引用：构造一棵小二叉树 ===")
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    print("  根 / 左 / 左左 的 value:", root.value, root.left.value, root.left.left.value)
    print("  叶子节点 right.left 是 None:", root.right.left is None)
    # 前面提过的标注瑕疵在这里现形：注解写的是 "TreeNode"（不含 None），
    # 可叶子的 left / right 实际就是 None，静态检查会认为类型不匹配。
    print("  __init__.__annotations__ 存的是字符串:", TreeNode.__init__.__annotations__)
    print("  get_type_hints 还原后:", get_type_hints(TreeNode.__init__))

    print("\n=== 5. 标注里到底存了什么 ===")
    print("  ToolResult.__annotations__:", ToolResult.__annotations__)
    print("  ToolHandler:", ToolHandler)
