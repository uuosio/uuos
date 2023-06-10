import os
import sys
import shlex
import platform
import subprocess
import sysconfig
import argparse
from . import run

__version__ = "0.4.1"

class CustomImporter(object):
    def find_module(self, fullname, mpath=None):
#        print('+++find_module', fullname)
        if fullname in ['_chain', '_chainapi', '_vm_api']:
            return self
        return

    def load_module(self, module_name):
#        print('+++load_module', module_name)
        from . import _eos        
        mod = sys.modules.get(module_name)
        if mod is None:
            uuos_module = sys.modules.get('ipyeos._eos')
            if not uuos_module:
                return
            uuos_so = uuos_module.__file__
            from importlib import util
            spec = util.spec_from_file_location(module_name, uuos_so)
            mod = util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            sys.modules[module_name] = mod
        return mod

sys.meta_path.append(CustomImporter())

if 'RUN_IPYEOS' in os.environ:
    from . import _eos
    import _chainapi
    import _chain
    import _vm_api

def run_ipyeos(custom_cmds=[]):
    return run.run_ipyeos(custom_cmds)

def run_eosnode():
    custom_cmds=['-m', 'ipyeos', 'eosnode']
    custom_cmds.extend(sys.argv[1:])
    return run.run_eosnode(custom_cmds)

def run_nodeos():
    run.run_program('nodeos')

def run_keosd():
    run.run_program('keosd')

def run_cleos():
    run.run_program('cleos')

def start_debug_server():
    return run.start_debug_server()

def run_test():
    if len(sys.argv) == 2:
        cmd = f'ipyeos -m pytest -s -x -o log_cli=true -o log_cli_level=INFO {sys.argv[1]}'
    elif len(sys.argv) == 3:
        cmd = f'ipyeos -m pytest -s -x -o log_cli=true -o log_cli_level=INFO {sys.argv[1]} -k {sys.argv[2]}'
    else:
        print('usage: eostest [test script] [test case]')
        return
    print(cmd)
    cmd = shlex.split(cmd)
    return subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr)
