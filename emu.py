import sys
import os
import importlib
import shutil
from py_utils.colors import COLORS
from py_utils.emu_utils import run, kill, error, warning, success, verify_fork_url, is_affirmative
from py_utils.emu_utils import SYSTEM_BASHRC_PATH, COMMUNITY_PATH, COMMUNITY_BASHRC_PATH, OH_MY_COMMA_PATH, UPDATE_PATH, OPENPILOT_PATH

sys.path.append(OPENPILOT_PATH)
DEBUG = not os.path.exists('/data/params/d')


class Command:
  def __init__(self, description=None, commands=None):
    self.description = description
    self.commands = commands

class Flag:
  def __init__(self, flags, description):
    self.flags = flags
    self.description = description

class CommandClass:
  debug_commands = {'controlsd': {'command': Command(description='logs controlsd to /data/output.log'),
                                  'flags': None}}

  commands = {'update':      {'command': Command(description='updates this tool, recommended to restart ssh session'),
                              'flags': None},
              'pandaflash':  {'command': Command(description='flashes panda with make recover'),
                              'flags': None},
              'pandaflash2': {'command': Command(description='flashes panda using Panda module'),
                              'flags': None},
              'debug':       {'command': Command(description='debugging tools', commands=debug_commands),
                              'flags': None},
              'installfork': {'command': Command(description='Specify the fork URL after. Moves openpilot to openpilot.old'),
                              'flags': [Flag(['l', 'lite'], 'Fast cloning, clones only the default branch with all commits flattened')]}}


class Emu:
  def __init__(self, args):
    self.args = args
    self.cc = CommandClass()

    self.arg_idx = 0
    self.parse()

  def _update(self):
    if not run(['sh', UPDATE_PATH]):
      error('Error updating!')

  def _pandaflash(self):
    r = run('make -C {}/panda/board recover'.format(OPENPILOT_PATH))
    if not r:
      error('Error running make command!')

  def _pandaflash2(self):
    if not run('pkill -f boardd'):
      error('Error killing boardd! Is it running?')
      return
    importlib.import_module('panda', 'Panda').Panda().flash()

  def _debug(self):
    cmd = self.get_next_arg()
    if cmd is None:
      print("You must specify a command for emu debug. Some options are:")
      self.print_commands('debug_commands')
      return
    if cmd not in self.cc.debug_commands:
      print('Unsupported debug command! Try one of these:')
      self.print_commands('debug_commands')
      return
    self.start_function_from_str(cmd)

  def _controlsd(self):
    # r = run('pkill -f controlsd')  # terminates file for some reason  # todo: remove me
    r = kill('selfdrive.controls.controlsd')  # seems to work, some process names are weird
    if r is None:
      warning('controlsd is already dead! (continuing...)')
    run('python {}/selfdrive/controls/controlsd.py'.format(OPENPILOT_PATH), out_file='/data/output.log')

  def _installfork(self):
    OPENPILOT_TEMP_PATH = '{}.temp'.format(OPENPILOT_PATH)
    clone_url = self.get_next_arg()
    if clone_url is None:
      error('You must specify a fork URL to clone!')
      return

    if not verify_fork_url(clone_url):  # verify we can clone before moving folder!
      error('The specified fork URL is not valid!')
      return

    if os.path.exists(OPENPILOT_TEMP_PATH):
      warning('{} already exists, should it be deleted to continue?'.format(OPENPILOT_TEMP_PATH))
      if is_affirmative():
        shutil.rmtree(OPENPILOT_TEMP_PATH)
      else:
        error('Exiting...')
        return

    # Clone fork to temp folder
    warning('Fork will be installed to {}'.format(OPENPILOT_PATH))
    try:  # catch ctrl+c and clean up after
      r = run('git clone {} {}'.format(clone_url, OPENPILOT_TEMP_PATH))  # clone to temp folder
    except:
      r = False

    # If openpilot.bak exists, determine a good non-exiting path
    # todo: make a folder that holds all installed forks and provide an interface of switching between them
    bak_dir = '{}.bak'.format(OPENPILOT_PATH)
    bak_count = 0
    while os.path.exists(bak_dir):
      bak_count += 1
      bak_dir = '{}.{}'.format(bak_dir, bak_count)

    if r:
      success('Cloned successfully! Installing fork...')
      shutil.move(OPENPILOT_PATH, bak_dir)  # move current installation to old dir
      shutil.move(OPENPILOT_TEMP_PATH, OPENPILOT_PATH)  # move new clone temp folder to main installation dir
      success('Installed! Don\'t forget to restart your device')
    else:
      error('\nError cloning specified fork URL!', end='')
      if os.path.exists(OPENPILOT_TEMP_PATH):  # git usually does this for us
        error(' Cleaning up...')
        shutil.rmtree(OPENPILOT_TEMP_PATH)
      else:
        print()

  def parse(self):
    if len(self.args) == 0:
      print('You must specify a command for emu. Some options are:')
      self.print_commands()
      return
    cmd = self.get_next_arg()
    if cmd not in self.cc.commands:
      print('Unsupported command! Try one of these:')
      self.print_commands()
      return

    self.start_function_from_str(cmd)

  def start_function_from_str(self, cmd):
    cmd = '_' + cmd
    if not hasattr(self, cmd):
      print('Command has not been implemented yet, please try updating.')
      return
    getattr(self, cmd)()  # call command's function

  def print_commands(self, command='commands'):
    cmd_list = getattr(self.cc, command)
    cmds = [cmd for cmd in cmd_list]
    to_print = []
    for cmd in cmds:
      desc = COLORS.CYAN + cmd_list[cmd]['command'].description
      # other format: to_append = '- {:>15}: {:>20}'.format(cmd, desc)
      to_append = '- {:<12} {}'.format(cmd + ':', desc)  # 12 is length of longest command + 1
      to_print.append(COLORS.OKGREEN + to_append)
    print('\n'.join(to_print) + COLORS.ENDC + '\n')

  def get_next_arg(self, lower=True):
    if len(self.args) - 1 < self.arg_idx:
      return None

    arg = self.args[self.arg_idx]
    self.arg_idx += 1

    if lower:
      arg = arg.lower()
    return arg


if __name__ == "__main__":
  args = sys.argv[1:]
  if DEBUG:
    args = input().split(' ')
    if '' in args:
      args.remove('')
  emu = Emu(args)