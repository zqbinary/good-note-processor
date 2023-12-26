def notify(msg='ok'):
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast("copy-copy", msg, duration=2)
    except TypeError as e:
        print('notify fail', str(e))
    except Exception as e:
        print('notify fail e', str(e))
