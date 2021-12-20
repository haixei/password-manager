from termcolor import cprint

def create_menu(title, subtitle, choices):
    cprint(title, 'blue', attrs=['bold'])
    print(subtitle + '\n')

    # Loop trough the options
    for i in range(len(choices)):
        cprint(str(i + 1) + '. ' + choices[i], 'blue')

    # Final index of the list, we always add the exit option at the end
    exit_index = len(choices) + 1
    cprint(str(exit_index) + '. Exit\n', 'blue')

    # Save the user's answer
    choice = input('Your choice: ')

    # If the answer is not a digit or it's not in the range of our options (from 1 to the exit index),
    # return an error
    if choice.isdigit() is not True or (int(choice) > exit_index or int(choice) <= 0):
        cprint('Your answer has to be a valid number, try again.', 'red')
        create_menu(title, subtitle, choices)
    else:
        # We know that the choice must be a digit so we can safely transform it to an integer
        # and have an easier time using the answer later
        choice = int(choice)
        if choice == exit_index:
            exit()
        return choice
