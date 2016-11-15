# Foris - web administration interface for OpenWrt based on NETCONF
# Copyright (C) 2016 CZ.NIC, z. s. p. o. <https://www.nic.cz>
#
# Foris is distributed under the terms of GNU General Public License v3.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from xml.etree import cElementTree as ET

from foris.nuci.modules.base import YinElement


class NuciDiagnostics(YinElement):
    tag = "diagnostics"
    NS_URI = "http://www.nic.cz/ns/router/diagnostics"

    @property
    def key(self):
        return "diagnostics"

####################################################################################################
ET.register_namespace("diagnostics", NuciDiagnostics.NS_URI)
