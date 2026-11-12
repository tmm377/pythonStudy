"""例一：带参数的装饰器 —— @repeat(3)

带参数的装饰器是三层嵌套：
    repeat(3)          -> 返回一个装饰器      （第一层，接参数）
    repeat(3)(greet)   -> 返回 wrapper        （第二层，接函数）
    greet = wrapper                            （第三层，接调用时的实参）

最外面那层不装饰任何东西，它只负责把参数存起来（闭包），
然后返回一个"标准的"两层装饰器。
"""

from functools import wraps


def repeat(times):
    """第一层：接收装饰器自己的参数，返回一个装饰器"""
    def decorator(func):
        """第二层：接收被装饰的函数，返回包装函数"""
        @wraps(func) # 作用：保留原函数的名字和文档，入参是传入的函数
        # TODO 学 AI 后端时，@app.get() 下面再套一层自定义装饰器（鉴权、限流），忘记写 @wraps 时会无声地使接口失效。这类 bug 很难排查，因为装饰器本身的逻辑完全正常。
        # FastAPI 这种靠函数签名工作的框架，会从参数名和注解推测出 query 参数、请求体。如果接口被一个没加 @wraps 的装饰器包住，它看到的是 (*args, **kwargs)
        def wrapper(*args, **kwargs):
            """第三层：真正被调用的那个，接住一切参数再转发"""
            results = []
            for i in range(times):
                print(f"  第 {i + 1}/{times} 次调用 {func.__name__}")
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator


@repeat(2)
def greet(name, greeting="你好"):
    print(f"    {greeting}，{name}")
    return f"{greeting}，{name}"


if __name__ == "__main__":
    print("=== @repeat(3) 带一个参数 ===")
    result = greet("明月")
    print("  返回值:", result)

    print()
    print("=== 换个参数，同一个装饰器 ===")
    # 注意：这里用一个全新函数，不要拿已装饰过的 greet 再套一层
    def say_hi(name):
        print(f"    hi, {name}")
        return name

    say_hi = repeat(2)(say_hi)        # 等价于在 say_hi 上加 @repeat(2)
    print("  返回值:", say_hi("青禾"))
