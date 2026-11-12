config = {
    "model": "deepseek-v3",
    "temperature": 0.7,
    "max_tokens": 4096
}

# 常用操作
print(config["model"])                   # 访问（key 不存在会报错）
print(config.get("top_p", 1.0))          # 安全访问（不存在返回默认值）
config["stream"] = True                  # 添加/修改
print(config.keys())                     # 所有键
print(config.values())                   # 所有值
print(config.items())                    # 所有键值对