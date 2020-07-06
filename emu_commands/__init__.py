import glob
import importlib
from py_utils.emu_utils import error
from os.path import dirname, basename, isfile, join
EMU_COMMANDS = []
import os
for module_name in os.listdir(os.path.dirname(__file__)):
    if module_name.endswith('.py') or module_name == '__pycache__':
        continue
    module = importlib.import_module('emu_commands.{}'.format(module_name))
    module = getattr(module, module_name.title())()
    EMU_COMMANDS.append(module)
    print(dir(module))
    print(module_name)

    # __import__(module[:-3], locals(), globals())
# raise Exception
# EMU_COMMANDS = []
# modules = glob.glob(join(dirname(__file__), "*.py"))
# __all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
# __all__.remove('base')
# print(__all__)
# print([basename(f)[:-3] for f in modules])
#
# for module_name in __all__:
#   try:
#     module = importlib.import_module('emu_commands.{}'.format(module_name))
#     module = getattr(module, module_name.title())()
#     EMU_COMMANDS.append(module)
#   except Exception as e:
#     error('Error loading {} command, please try updating!'.format(module_name))
#     error(e)
