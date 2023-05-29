import core.options as options
import core.commands as commands
import core.exceptions as exceptions

def execute_option(option_type, args):
    
    if option_type in ('-a', '--add'):
        if not args:
            raise exceptions.ArgumentError("No arguments given")
        options.add(args)

    if option_type in ('-f', '--force'):
        options.add(args)

def execute_command(option_command, **kargs):
    if option_command in ('merge'):
        commands.merge.execute()

def is_command_or_option(arg):
    """Return True if arg is a command or an option"""
    return arg in options.option_list or arg in commands.command_list


def detailed_args(argv : list[str]) -> dict:
    args = {
        "options" : list(),
        "commands" : list()
    }
    iter_argv = iter(argv)
    arg = next(iter_argv)
    
    while True:
        if arg in options.option_list:
            option_type = arg
            option_arg_list = []
            
            while (option_arg := next(iter_argv, None)) is not None and not is_command_or_option(option_arg):
                option_arg_list.append(option_arg)
            args["options"].append([option_type, option_arg_list])

        if arg in commands.command_list:
            args["commands"].append([arg])        
        try :
            arg = next(iter_argv)
        except StopIteration:
            break
    return args



def execute_from_command_line(argv : list[str]):
    
    argv_detailed = detailed_args(argv)
    for option in argv_detailed["options"]:
        execute_option(*option)

    for command in argv_detailed["commands"]:
        execute_command(*command)

