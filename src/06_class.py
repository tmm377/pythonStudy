class Agent:
    """AI Agent基类"""

    category = "AI"

    __mm = "aa"

    __mm__ = "调得到"

    def __init__(self, name="wuming", model="gpt-4"):
        self.name = name
        self.model = model
        self._memory = []

    def introduce(self):
        return f"我是{self.name}，使用{self.model}模型"

    def __str__(self):
        return f"Agent__str__({self.name})"

    def __repr__(self):
        return f"Agent__repr__(name='{self.name}',model='{self.model}')"


class CodingAgent(Agent):
    def __init__(self, name, model="gpt-4", languages=None):
        super().__init__(name, model)
        self.languages = languages or ["Python"]

    def code_review(self, code: str) -> str: # 注解不产生任何运行时行为
        # print(self.introduce())
        return f"[{self.name},{code}]"
    # 扩展父类的方法
    def introduce(self):
        print(super().__mm__) # 调得到__mm__
        print(super().__mm) #调不到__mm
        print(super().__str__())
        return f"{super().introduce()},会{len(self.languages)}门语言"

agent = CodingAgent("mingyue",languages=["Python", "TypeScript"])
print(agent.introduce())
print(agent.category)
print(agent.code_review("print('hello')"))
print(agent.code_review(None))