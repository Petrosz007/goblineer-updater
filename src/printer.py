import sys, os

def start_process_print(str):
    sys.stdout.write('\r[ ] ' + str)

def success_process_print(str):
    sys.stdout.flush()

    # Coloring doesn't work on windows, so it is disabled on windows
    if os.name == 'nt':
        sys.stdout.write('\r[{}] '.format('\u2713') + str + '\n')
    else:
        sys.stdout.write('\r[{}] '.format('\033[92m'+'\u2713'+'\033[0m') + str + '\n')

def error_process_print(str):
    sys.stdout.flush()
    
    # Coloring doesn't work on windows, so it is disabled on windows
    if os.name == 'nt':
        sys.stdout.write('\r[{}] '.format('X') + str + '\n')
    else:
        sys.stdout.write('\r[{}] '.format('\033[91m'+'X'+'\033[0m') + str + '\n')
