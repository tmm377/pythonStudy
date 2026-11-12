"""例四：去掉 @ 语法糖，本质是函数调用

    @repeat(2)                 @simple_log
    def hello(): ...           def hello(): ...
    ↓                          ↓
    hello = repeat(2)(hello)   hello = simple_log(hello)

@ 一行里藏了两次调用。带参数的装饰器那一行之所以有三层，
就是因为括号要连着开两次：第一次给参数，第二次给函数。
"""

from functools import wraps


def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for i in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator


def hello():
    print("    hello")
    return "ok"


if __name__ == "__main__":
    print("=== 1. 看看 repeat(2) 到底返回了什么 ===")
    d = repeat(2)
    print("  repeat(2)       ->", d)
    print("  类型            ->", type(d).__name__)

    print()
    print("=== 2. 它是个装饰器，喂给它函数就得到 wrapper ===")
    w = d(hello)
    print("  repeat(2)(hello) ->", w)
    print("  原来的 hello      ->", hello)

    print()
    print("=== 3. 手动完成 @ 干的事：把名字换掉 ===")
    hello = repeat(2)(hello)          # 这一行等价于 @repeat(2)
    print("  调用 hello() =>")
    hello()

    print()
    print("=== 4. 所以 @ 只是函数调用的简写 ===")
    print("  @repeat(2)  ==  hello = repeat(2)(hello)")
