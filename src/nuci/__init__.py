# Foris - web administration interface for OpenWrt based on NETCONF
# Copyright (C) 2016 CZ.NIC, z. s. p. o. <https://www.nic.cz>
#
# Foris is distributed under the terms of GNU General Public License v3.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging

from xml.etree import cElementTree as ET
from foris.nuci.client import dispatch
from ncclient.operations import RPCError, TimeoutExpiredError

from . import diagnostics_module as diagnostics

logger = logging.getLogger(__name__)


def get_diagnostics_modules():
    try:
        data = dispatch(diagnostics.Modules.rpc_list_modules())
        return diagnostics.Modules.from_element(ET.fromstring(data.xml))
    except (RPCError, TimeoutExpiredError):
        return None


def get_diagnostics():
    try:
        data = dispatch(diagnostics.List.rpc_list_diagnostics())
        return diagnostics.List.from_element(ET.fromstring(data.xml))
    except (RPCError, TimeoutExpiredError):
        return None


def get_diagnostic(diag_id):
    try:
        data = dispatch(diagnostics.Show.rpc_get(diag_id))
        return diagnostics.Show.from_element(ET.fromstring(data.xml))
    except (RPCError, TimeoutExpiredError):
        return None


def remove_diagnostic(diag_id):
    try:
        dispatch(diagnostics.Remove.rpc_remove(diag_id))
        return True
    except (RPCError, TimeoutExpiredError):
        return False
