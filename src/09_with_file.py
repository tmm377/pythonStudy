"""with 的基础：它解决的是"清理被异常跳过"

没有 with：open 之后如果中途抛异常，close 那行永远执行不到。
有 with：无论正常结束、抛异常、return 还是 break，__exit__ 都会执行。
"""

import os


def leak_demo():
    """没有 with：异常发生时 f.close() 执行不到"""
    path = "/tmp/_with_leak.txt"
    try:
        f = open(path, "w", encoding="utf-8")
        f.write("hello")
        raise RuntimeError("中途出错")
        f.close()                       # ← 永远执行不到
    except RuntimeError as e:
        print("  异常:", e)
        print("  文件是否已关闭:", f.closed, " ← 泄漏")
        f.close()
        print("  手动补救后:", f.closed)
    finally:
        os.remove(path)


def safe_demo():
    """有 with：异常照常抛出，但文件已经被关掉"""
    path = "/tmp/_with_safe.txt"
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("hello")
            raise RuntimeError("又出错了")
    except RuntimeError as e:
        print("  异常:", e)
        print("  离开 with 之后 f.closed =", f.closed, " ← 自动关了")
    finally:
        os.remove(path)


if __name__ == "__main__":
    print("=== 1. 没有 with ===")
    leak_demo()

    print()
    print("=== 2. 有 with ===")
    safe_demo()

    print()
    print("=== 3. 正常结束也一样会关 ===")
    os.makedirs("/tmp/_with_dir", exist_ok=True)
    p = "/tmp/_with_dir/a.txt"
    with open(p, "w", encoding="utf-8") as f:
        f.write("正常写")
    print("  退出块后 f.closed =", f.closed)
    with open(p, encoding="utf-8") as f:
        print("  读回来:", f.read())
