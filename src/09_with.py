import time

class TimerContext:
    """一个计时上下文管理器"""
    def __enter__(self):
        self.start = time.time()
        return self
        # return self 作用：__enter__ 的返回值会赋给 as 后面的变量。你没写 as，所以它被丢掉了。写成 with TimerContext() as t: 之后，块内块外都能读 t.start、t.elapsed（如果你想把耗时存成属性而不是直接 print）

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start
        print(f"执行耗时：{elapsed:.3f} 秒")
        return False  # False = 不抑制异常（让异常正常传播）

# 使用
with TimerContext():
    total = sum(range(10_000_000))  # 耗时操作
# 输出：执行耗时：0.xxx 秒

# 先打印耗时再抛错，__exit__ 没被异常跳过
with TimerContext():
    raise ValueError("故意出错")
# 输出：执行耗时：0.000 秒
# Traceback (most recent call last):
#   File "/Users/mmtian/Documents/workspace/pythonStudy/src/09_with.py", line 21, in <module>
#     raise ValueError("故意出错")
# ValueError: 故意出错