from colorama import Fore, Style


def status(msg):
    print(Style.DIM + msg + Style.RESET_ALL)

def info(msg):
    print(Fore.YELLOW + '[INFO] ' + Style.RESET_ALL + msg)

def done(msg):
    print('[DONE] ' + msg)

def success(msg):
    print(Fore.GREEN + msg + Style.RESET_ALL)

def error(msg):
    print(Fore.RED + '[ERROR] ' + Style.RESET_ALL + msg)

def continue_prompt(
    msg='Are you sure you want to continue? [Y/n] ',
    default='y',
):
    answer = input(Fore.YELLOW + msg + Style.RESET_ALL)
    if not answer:
        answer = default
    return answer.lower() == 'y'
