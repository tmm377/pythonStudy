# print("-----1-----")
# for n in range(2,10):
#     for x in range(2,n):
#         print(n)
print("-----方法一:现实中容易产生歧义，不常用-----")
for n in range(2,10):
    for x in range(2,n):
        if(n%x==0):
            break
    else: # else 是「循环没被 break 打断」时才执行的块
        print(f"{n}是质数")
