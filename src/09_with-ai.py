"""用 with 管理「AI 工具调用会话」：确保资源一定被释放

类版上下文管理器的三个关键点：
    1. __enter__ 负责准备（初始化状态、拿资源），返回值交给 as
    2. __exit__ 负责收尾（汇总 + 释放资源），无论正常还是异常都会执行
    3. __exit__ 返回 False（或不写 return）→ 异常照常传播，不被吞掉

真实项目里 __enter__ 拿到的可能是 HTTP 连接池、数据库句柄、临时文件；
这里用 io.StringIO 模拟「用完必须 close 的资源」，避免产生真实文件和网络请求。
"""

import io


def search_web(query):
    """占位工具函数：真实项目里这里会真的去联网检索。"""
    return f"搜索结果：{query}"


def read_file(path):
    """占位工具函数：真实项目里这里会真的读文件。"""
    return f"文件内容：{path}"


class ToolSession:
    """一次工具调用会话：收集结果，并在退出时释放资源。"""

    def __init__(self):
        # 「创建对象」阶段：先初始化状态，此时还没进入 with。
        # 放在 __init__ 而不是 __enter__，就算不写 with 也不会 AttributeError。
        self.results = []
        self._buffer = None          # 进入 with 之后才会拿到资源

    def __enter__(self):
        print("[Session] 开始工具调用会话")
        self._buffer = io.StringIO()  # 模拟需要释放的资源
        return self                   # `as session` 拿到的就是这个实例本身

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 三个参数依次是 (异常类型, 异常对象, traceback)。
        # 正常结束时全是 None，所以可以用来判断这次会话是否顺利。
        # 用 try/finally 兜底：就算汇总打印出错，close 也一定会执行。
        try:
            status = f"（因 {exc_type.__name__} 中断）" if exc_type else ""
            print(f"[Session] 会话结束{status}，共执行 {len(self.results)} 次工具调用")
            print("  结果:", self.results)
        finally:
            # 真正的清理。换成真实项目就是 conn.close() / f.close() / os.remove()
            self._buffer.close()
            print(f"[Session] 资源已释放: closed={self._buffer.closed}")

        # 不写 return 就是返回 None，效果等同 False → 异常照常往外抛。
        # 这里显式写出来是为了讲清楚意图；若返回 True，块内异常会被悄悄吞掉。
        return False


if __name__ == "__main__":
    print("=== 1. 正常路径 ===")
    with ToolSession() as session:
        session.results.append(search_web("AI Agent"))
        session.results.append(read_file("config.json"))
    # with 不会创建新的作用域，块结束后 session 变量依然可以访问。
    print("  as 拿到的对象类型:", type(session).__name__)

    print()
    print("=== 2. 异常路径：收尾照做，异常照样传出 ===")
    try:
        with ToolSession() as session:
            session.results.append(search_web("AI Agent"))
            raise RuntimeError("工具调用失败")
    except RuntimeError as e:
        print("  外层接住异常:", e)
