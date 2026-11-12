# pythonStudy

明月的 Python 学习项目。**现在是空的，往里加什么由你决定。**

## 跑起来

```bash
cd ~/Documents/workspace/pythonStudy
source .venv/bin/activate      # 命令行前面出现 (.venv)
python src/main.py
deactivate
```

不想激活也行：`./.venv/bin/python src/main.py`

## 目录

```
src/          你的代码。加东西就加在这
playground/   草稿区，随便试，改坏了不心疼
.venv/        Python 环境（已建好，装什么都不会污染系统）
.gitignore    已配好，别提交 .venv
```

`notes/`、`tests/` 这些等真需要了再自己建，别一上来铺一堆空目录。

## 往里加东西的规矩（三条）

**1. 一个知识点一个文件，编号递增**

```
src/01_变量与类型.py     ← 不好：中文文件名在某些工具里会出岔子
src/01_types.py          ← 好
src/02_lists.py
```

编号让你随时知道自己走到哪，也保证顺序不会乱。

**2. 每个文件都能单独跑**

`python src/02_lists.py` 直接出结果。别写那种"必须先跑 A 才能跑 B"的代码，学习阶段那是自找麻烦。

**3. 跑不通的不算写完**

看懂 ≠ 会。能跑通、能改坏、能改回来，才算。

## 环境备忘

- Python **3.13.7**，来自 `/Library/Frameworks/Python.framework/`
- 系统自带的 `/usr/bin/python3` 是 3.9，别用它
- 装依赖：`pip install 包名`（激活环境后）
- 记下装了什么，或者以后换成 `uv`，一句 `uv add` 就自动记

## Git

已经 `git init` 过了，还没提交。第一次提交留给你自己敲：

```bash
git add .
git commit -m "init: 空的开始"
```

以后每学完一个知识点提交一次。**提交历史就是你真实的学习曲线**，比任何打卡都诚实。
