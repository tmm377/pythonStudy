# ========== 列表推导式 ==========

# 普通写法
squares = []
for i in range(10):
    print(i * 2)
# 推导式写法
squares = [i ** 2 for i in range(10)]
print(squares)

# 条件过滤式写法
events = [i*2 for i in range(20) if i % 2 == 0]
print(events)

# 嵌套循环
pairs = [(x,y) for x in 'ab' for y in 'cd']
print(pairs)

# 字典推导式
tool_map = {
    "search": "搜索网络",
    "read": "读取文件",
    "write": "写入文件",
}
# 可以调转键值对
reversed_map = {v:k for k,v in tool_map.items()}
print(reversed_map)

# 有序集合推导式
unique_lengths= {len(word) for word in ["ai", "agent", "python", "code"]}
print(unique_lengths)

# 圆括号写法
big_sum = sum(i for i in range(1_000))
print(big_sum)


