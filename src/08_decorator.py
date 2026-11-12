import time

def timing_decoratore(func):
    """测量执行时间的装饰器"""
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        elapesd = time.time() - start
        print(f"[计时]{func.__name__}执行耗时：{elapesd:.3f}秒")
        return ret
    return wrapper

@timing_decoratore
def slow_function():
    time.sleep(2)
    #return 'fine'

print(slow_function())