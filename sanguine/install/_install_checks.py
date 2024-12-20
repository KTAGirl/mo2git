import importlib
import subprocess

# for install_checks we cannot use any files with non-guaranteed dependencies, so we:
#                    1. may use only those Python modules installed by default, and
#                    2. may use only those sanguine modules which are specifically designated as install-friendly
from sanguine.install.install_common import *

REQUIRED_PIP_MODULES = ['json5', 'bethesda-structs', 'pywin32']
PIP2PYTHON_MODULE_NAME_REMAPPING = {'bethesda-structs': 'bethesda_structs', 'pywin32': ['win32api', 'win32file']}


def _is_module_installed(module: str) -> bool:
    try:
        importlib.import_module(module)
        return True
    except ImportError:
        return False


def _not_installed(msg: str) -> None:
    critical(msg)
    critical('Aborting. Please make sure to run sanguine-rose/sanguine-install.py')
    # noinspection PyProtectedMember, PyUnresolvedReferences
    os._exit(1)


def _check_module(m: str) -> None:
    if not _is_module_installed(m):
        _not_installed('Module {} is not installed.'.format(m))


def check_sanguine_prerequisites(frominstall: bool = False) -> None:
    # we don't really need to check for MSVC being installed, as without it some of the pip modules won't be available

    for m in REQUIRED_PIP_MODULES:
        if m in PIP2PYTHON_MODULE_NAME_REMAPPING:
            val = PIP2PYTHON_MODULE_NAME_REMAPPING[m]
            if isinstance(val, list):
                for v in val:
                    _check_module(v)
            else:
                _check_module(val)
        else:
            _check_module(m)

    if subprocess.call(['git', '--version']) != 0:
        critical('git is not found in PATH.')
        critical(
            '{}Please make sure to install "Git for Windows" or "GitHub Desktop" (preferred) and include folder with git.exe into PATH.'.format(
                'Aborting. ' if frominstall else ''
            ))
        # noinspection PyProtectedMember, PyUnresolvedReferences
        os._exit(1)

    info('All sanguine prerequisites are ok.')
