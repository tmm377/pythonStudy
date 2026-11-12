def log_tool_call(func):
    def wrapper(*args, **kwargs):
        print(f"  [Tool] {func.__name__}(args={args}, kwargs={kwargs})")
        result = func(*args, **kwargs)
        print(f"  [Tool] {func.__name__} 返回 {result[:50]}...")
        return result
    return wrapper

@log_tool_call
def search_web(query:str)->str:
    return f"搜索结果：关于'{query}'的10条相关信息..."

if __name__ == "__main__":
    resu = search_web('小红')
    print(resu)