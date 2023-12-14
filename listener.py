# 创建 KeyListener 实例，启动监听
from service.KeyListener import KeyListener


def main():
    listener = KeyListener()
    listener.setup_listener()


if __name__ == "__main__":
    main()
