
print("-----方法二-----")
# all() 只做一件事：把一堆条件合并成一个布尔值。
  # 遇到第一个假值，all() 立刻返回 False，剩下的元素连算都不算
# if 再根据这个返回值决定要不要执行
for n in range(2, 10):
    if all(n % x != 0 for x in range(2, n)):
        print(f"{n} 是质数")
