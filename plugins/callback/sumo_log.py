# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Inspired from: https://github.com/redhat-openstack/khaleesi/blob/master/plugins/callbacks/human_log.py
# Further improved support Ansible 2.0

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import json
import logging
import time

#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

from ansible.module_utils._text import to_bytes
from ansible.plugins.callback import CallbackBase

'''
try:
    import simplejson as json
except ImportError:
    import json
'''

#logfile = '/Users/dgadoury/github/ansible-to-sumo/ansible.log'

log = logging.getLogger('ansible')
#fh = logging.FileHandler('/Users/dgadoury/github/ansible-to-sumo/ansible.log')
#logger.addHandler(fh)

#log = logging.basicConfig(filename=logfile)

# Fields to reformat output for
FIELDS = ['cmd', 'command', 'start', 'end', 'delta', 'msg', 'stdout',
          'stderr', 'results']


class CallbackModule(CallbackBase):

    """
    Ansible callback plugin for human-readable result logging for log aggregators
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'human_log'
    #CALLBACK_NEEDS_WHITELIST = False
    CALLBACK_NEEDS_WHITELIST = True 

    TIME_FORMAT = "%b %d %Y %H:%M%:%S"
    MSG_FORMAT = "- %host(s) - %(data)s\n\n"
    #MSG_FORMAT = "%(now)s - %(host)s - %(data)s\n\n"
    MSG_FORMAT_NO_HOST = "%(data)s"
    #MSG_FORMAT_NO_HOST = "%(now)s - %(data)s\n\n"
    #MSG_FORMAT="%(now)s - %(category)s - %(data)s\n\n"

    def __init__(self):

        super(CallbackModule, self).__init__()
    '''
    def log(self, data):
        if type(data) == dict:
            for field in FIELDS:
                no_log = data.get('_ansible_no_log')
                if field in data.keys() and data[field] and no_log != True:
                    output = self._format_output(data[field])
                    print("\n{0}: {1}".format(field, output.replace("\\n","boogers\n")))
    '''

    def log(self, data, host=None):
    #def log(self, host, category, data):
        if type(data) == dict:
            if '_ansible_verbose_override' in data:
                # avoid logging exteranous data
                data = 'omitted'
            else:
                data = data.copy()
                invocation = data.pop('invocation', None)
                data = json.dumps(data)
                if invocation is not None:
                    data = json.dumps(invocation) + " => %s " % data

        now = time.strftime(self.TIME_FORMAT, time.localtime())
        
        if host is None:
            msg = to_bytes(self.MSG_FORMAT_NO_HOST % dict(data=data))
        else:
            msg = to_bytes(self.MSG_FORMAT % dict(host=host, data=data))
        #msg = to_bytes(self.MSG_FORMAT % dict(now=now, category=category, data=data))

        log.info(msg)

    '''
    def _format_output(self, output):
        # Strip unicode
        if type(output) == unicode:
            output = output.encode(sys.getdefaultencoding(), 'replace')

        # If output is a dict
        if type(output) == dict:
            return json.dumps(output, indent=2)

        # If output is a list of dicts
        if type(output) == list and type(output[0]) == dict:
            # This gets a little complicated because it potentially means
            # nested results, usually because of with_items.
            real_output = list()
            for index, item in enumerate(output):
                copy = item
                if type(item) == dict:
                    for field in FIELDS:
                        if field in item.keys():
                            copy[field] = self._format_output(item[field])
                real_output.append(copy)
            return json.dumps(output, indent=2)

        # If output is a list of strings
        if type(output) == list and type(output[0]) != dict:
            # Strip newline characters
            real_output = list()
            for item in output:
                if "\n" in item:
                    for string in item.split("\n"):
                        real_output.append(string)
                else:
                    real_output.append(item)

            # Reformat lists with line breaks only if the total length is
            # >75 chars
            if len("".join(real_output)) > 75:
                return "\n" + "\n".join(real_output)
            else:
                return " ".join(real_output)

        # Otherwise it's a string, (or an int, float, etc.) just return it
        return str(output)
        '''


    def on_any(self, *args, **kwargs):
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        self.log(res, host)

    def runner_on_ok(self, host, res):
        self.log(res, host)

    def runner_on_skipped(self, host, item=None):
        pass

    def runner_on_unreachable(self, host, res):
        self.log(res, host)

    def runner_on_no_hosts(self):
        pass

    def runner_on_async_poll(self, host, res, jid, clock):
        self.log(res, host)

    def runner_on_async_ok(self, host, res, jid):
        self.log(res, host)

    def runner_on_async_failed(self, host, res, jid):
        self.log(res, host)

    def playbook_on_start(self):
        pass

    def playbook_on_notify(self, host, handler):
        pass

    def playbook_on_no_hosts_matched(self):
        pass

    def playbook_on_no_hosts_remaining(self):
        pass

    def playbook_on_task_start(self, name, is_conditional):
        pass

    def playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None):
        pass

    def playbook_on_setup(self):
        pass

    def playbook_on_import_for_host(self, host, imported_file):
        pass

    def playbook_on_not_import_for_host(self, host, missing_file):
        pass

    def playbook_on_play_start(self, name):
        pass

    def playbook_on_stats(self, stats):
        pass

    def on_file_diff(self, host, diff):
        pass


    ####### V2 METHODS ######
    def v2_on_any(self, *args, **kwargs):
        pass

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.log(result._result)

    def v2_runner_on_ok(self, result):
        self.log(result._result)

    def v2_runner_on_skipped(self, result):
        self.log(result._result)
        #pass

    def v2_runner_on_unreachable(self, result):
        self.log(result._result)

    def v2_runner_on_no_hosts(self, task):
        self.log(result._result)
        #pass

    def v2_runner_on_async_poll(self, result):
        self.log(result._result)

    def v2_runner_on_async_ok(self, host, result):
        self.log(result._result, host)

    def v2_runner_on_async_failed(self, result):
        self.log(result._result)

    def v2_playbook_on_start(self, playbook):
        pass

    def v2_playbook_on_notify(self, result, handler):
        self.log(result._result)
        pass

    def v2_playbook_on_no_hosts_matched(self):
        pass

    def v2_playbook_on_no_hosts_remaining(self):
        pass

    def v2_playbook_on_task_start(self, task, is_conditional):
        pass

    def v2_playbook_on_vars_prompt(self, varname, private=True, prompt=None,
                                   encrypt=None, confirm=False, salt_size=None,
                                   salt=None, default=None):
        pass

    def v2_playbook_on_setup(self):
        pass

    def v2_playbook_on_import_for_host(self, result, imported_file):
        pass

    def v2_playbook_on_not_import_for_host(self, result, missing_file):
        pass

    def v2_playbook_on_play_start(self, play):
        pass

    def v2_playbook_on_stats(self, stats):
        pass

    def v2_on_file_diff(self, result):
        self.log(result._result)
        #pass

    def v2_playbook_on_item_ok(self, result):
        self.log(result._result)
        #pass

    def v2_playbook_on_item_failed(self, result):
        iself.log(result._result)
        #pass

    def v2_playbook_on_item_skipped(self, result):
        self.log(result._result)
        #pass

    def v2_playbook_on_include(self, included_file):
        pass

    def v2_playbook_item_on_ok(self, result):
        self.log(result._result)
        #pass

    def v2_playbook_item_on_failed(self, result):
        self.log(result._result)
        #pass

    def v2_playbook_item_on_skipped(self, result):
        self.log(result._result)
        #pass
