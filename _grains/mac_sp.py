# -*- coding: utf-8 -*-
'''
Mac hardware information, generated by system_profiler.

This is a separate grains module because it has a dependency on plistlib.
'''

import logging
import salt.utils
import salt.modules.cmdmod

log = logging.getLogger(__name__)

__virtualname__ = 'mac_sp'

try:
    import plistlib
    has_libs = True
except ImportError:
    has_libs = False

def __virtual__():
    if salt.utils.is_darwin() and has_libs:
        return __virtualname__
    else:
        return False

# Chicken and egg problem, SaltStack style
# __salt__ is already populated with grains by this stage.
cmdmod = {
    'cmd.run': salt.modules.cmdmod._run_quiet,
    # 'cmd.retcode': salt.modules.cmdmod._retcode_quiet,
    'cmd.run_all': salt.modules.cmdmod._run_all_quiet
}


def _get_spdatatype(sp_data_type):
    '''
    Run system_profiler with a specific data type.
    Running with all types slows down execution a bit, so be picky about what you need.
    '''
    output_plist = cmdmod['cmd.run']('system_profiler {0} -xml'.format(sp_data_type))
    return output_plist


def hardware():
    '''
    Get general hardware information.
    Provided by SPHardwareDataType (/System/Library/SystemProfiler/SPPlatformReporter.spreporter)
    '''
    sp_hardware = _get_spdatatype('SPHardwareDataType')
