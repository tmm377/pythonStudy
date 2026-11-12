tags = {"python", "agent", "llm"}

tags.add("fastapi")
print(tags)
tags.remove("llm")
print(tags)
print("python" in tags)

a={1,2,3}
b={2,3,4}
print(a&b) # 交集 {2.3}
print(a|b) # 并集 {1,2,3,4}
print(a-b) # 差集 {1}