from win10toast import ToastNotifier


def notify(msg='ok'):
    toaster = ToastNotifier()
    try:
        toaster.show_toast("copy-copy", msg, duration=2)
    except TypeError:
        pass

