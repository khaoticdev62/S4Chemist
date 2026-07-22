import sims4.commands
import services


@sims4.commands.Command('your.command.here', command_type=sims4.commands.CommandType.Live)
def your_command(_connection=None):
    output = sims4.commands.output(_connection)
    output('Hello from mod script!')
