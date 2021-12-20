from menu import create_menu
from vault_utils import create_new, retrieve_data, remove_password


def restart_after_task():
    answer = create_menu('\nTask finished.', 'What do you want to do?', ['Return to the main menu'])
    if answer == 1:
        start()


def start():
    title = '\nPassword manager.'
    subtitle = 'You are welcome to choose one of the following options.'
    options = ['Generate new password', 'View all passwords', 'Remove password']

    answer = create_menu(title, subtitle, options)
    if answer == 1:
        create_new()
        restart_after_task()
    elif answer == 2:
        retrieve_data()
        restart_after_task()
    elif answer == 3:
        remove_password()
        restart_after_task()


if __name__ == '__main__':
    start()
