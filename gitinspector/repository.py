# coding: utf-8
#
# Copyright © 2014 Ejwa Software. All rights reserved.
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

import os
import shutil
import subprocess
import sys
import tempfile

from urllib.parse import urlparse
from .messages import error, warning, debug
from .utils import run_cmd

class GitCloneFailed(Exception):
    def __init__(self, msg):
        super(GitCloneFailed, self).__init__(msg)
        self.msg = msg


class new_Repository():
    """A Repository holds the content of """

    def __init__(self, path):
        # Detect if 'path' is either a fs path or an url
        from urllib.parse import urlparse
        parsed_url = urlparse(path)

        # If the repo needs to get cloned from remote
        if parsed_url.scheme == "git" or parsed_url.scheme == "ssh" or \
           parsed_url.scheme == "http" or parsed_url.scheme == "https":
            from tempfile import TemporaryDirectory
            clone_path = TemporaryDirectory().name
            clone_cmd = ['git', 'clone', path, clone_path]
            retcode, stdout, stderr = run_cmd(clone_cmd)
            if retcode != 0:
                GitCloneFailed("command 'git clone %s %s' failed!\n" \
                               % (path, clone_path))
            self.path = clone_path
        else:
            # Default if scheme is None of 'file'
            self.path = parsed_url.path



class Repository(object):
    cloned_paths = []  # List of paths of temporary repositories

    def __init__(self, name, location, config):
        self.name = name
        self.location = location
        self.config = config

    @classmethod
    def create(cls, url, config):
        parsed_url = urlparse(url)

        if parsed_url.scheme == "file" or parsed_url.scheme == "git" or parsed_url.scheme == "http" or \
           parsed_url.scheme == "https" or parsed_url.scheme == "ssh":
            path = tempfile.mkdtemp(suffix=".gitinspector")
            git_clone = subprocess.Popen(["git", "clone",
                                          "-b " + config.branch,
                                          url, path],
                                         bufsize=1, stdout=sys.stderr)
            git_clone.wait()

            if git_clone.returncode != 0:
                error("%s: Unable to clone git repository." % path)

            cls.cloned_paths.append(path)
            return Repository(os.path.basename(parsed_url.path), path, config)
        else:
            return Repository(None, os.path.abspath(url), config)

    @classmethod
    def delete_all(cls):
        for path in cls.cloned_paths:
            shutil.rmtree(path, ignore_errors=True)

    def authors(self):
        authors_cmd = subprocess.Popen(["git", "-C", self.location, "shortlog",
                                        "-esn", self.config.branch],
                                       bufsize=1, stdout=subprocess.PIPE)
        rows = authors_cmd.stdout.readlines()
        authors_cmd.wait()
        authors_cmd.stdout.close()

        authors = []
        for row in rows:
            line = row.decode("utf-8", "replace").strip()
            authors.append(line.split('\t')[1])
        return authors
