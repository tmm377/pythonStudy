tools = ["search", "read_file", "write_code"]
mixed = [1, "hello", True, None]  # 可以混合类型

tools.append("execute")           # 尾部添加
print(tools)         
tools.insert(0, "plan")           # 指定位置插入
print(tools)                   
tools.pop()                       # 移除并返回最后一个
print(tools) 
print(tools[0])                   # 索引访问（从 0 开始）
print(tools[-1])                  # 倒数第一个
print(tools[1:3])                 # 切片：[1] 和 [2]