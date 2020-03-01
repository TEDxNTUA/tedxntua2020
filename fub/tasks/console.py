from colorama import Fore, Style


def status(msg):
    print(Style.DIM + msg + Style.RESET_ALL)

def info(msg):
    print(Fore.YELLOW + '[INFO] ' + Style.RESET_ALL + msg)

def done(msg):
    print('[DONE] ' + msg)

def success(msg):
    print(Fore.GREEN + msg + Style.RESET_ALL)
