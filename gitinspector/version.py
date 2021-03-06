# coding: utf-8
#
# Copyright © 2019 Emmanuel Fleury. All rights reserved.
# Copyright © 2012-2015 Ejwa Software. All rights reserved.
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

"""
This module encapsulate all what is related to version number and
how to display the version message to the user.
"""

import sys

from . import localization
localization.init()

__version__ = "2.0"

__doc__ = _("""Copyright © 2019 Emmanuel Fleury. All rights reserved.
Copyright © 2012-2015 Ejwa Software. All rights reserved.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
""")

def display():
    """Display version message to the user."""
    sys.stdout.write("gitinspector {0}\n".format(__version__) + __doc__)
    sys.exit(0)
