from emu_commands.fork import Fork
from emu_commands.update import Update
from emu_commands.panda import Panda
from emu_commands.debug import Debug
from emu_commands.info import Info
from emu_commands.uninstall import Uninstall


EMU_COMMANDS = [Fork(), Update(), Panda(), Debug(), Info(), Uninstall()]
