# 创建
point = (3, 4)
single = (1,)    # ← 单个元素的元组必须加逗号！

# 用途：函数返回多个值、作为字典的键、表示不会被修改的数据
def get_coordinates():
    return (116.40, 39.90)   # 实际返回的是一个元组

lat, lng = get_coordinates()  # 解包（unpacking）
print(lat, lng)