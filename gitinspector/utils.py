# coding: utf-8
#
# Copyright © 2019 Emmanuel Fleury. All rights reserved.
#
# This file is part of gitinspector.
#
# gitinspector is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gitinspector is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gitinspector. If not, see <http://www.gnu.org/licenses/>.

from subprocess import Popen, PIPE

# Return codes
RETURN_SUCCESS = 0
RETURN_FAILURE = 1

def run_cmd(cmd):
    """Run a process with 'cmd' and return (retcode, stdout, stderr)"""

    # Initialize Command Process
    try:
        cmd_process = Popen(cmd, bufsize=1,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        return (RETURN_FAILURE, "", "")

    # Run Command Process
    cmd_std, cmd_err = cmd_process.communicate()

    return (cmd_process.returncode,
            cmd_std.decode('utf-8', errors="ignore"),
            cmd_err.decode('utf-8', errors="ignore"))
