def greet(name, greeting="Hello"):
    """向某人打招呼。（这是 docstring）"""
    return f"{greeting}, {name}!"

print(greet("World"))

# 3. 可变参数 *args（接收任意数量的位置参数，打包成元组）
def sum_all(*args):
    print(args)
    return sum(args)

print(sum_all(1, 2, 3, 4))  # 10

# 4. 关键字参数 **kwargs（接收任意数量的关键字参数，打包成字典）
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", role="Engineer")