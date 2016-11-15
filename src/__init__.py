# Foris - web administration interface for OpenWrt based on NETCONF
# Copyright (C) 2016 CZ.NIC, z. s. p. o. <https://www.nic.cz>
#
# Foris is distributed under the terms of GNU General Public License v3.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os

from foris.config import ConfigPageMixin, add_config_page
from foris.config_handlers import BaseConfigHandler
from foris.plugins import ForisPlugin


class DiagnosticsConfigHandler(BaseConfigHandler):
    pass


class DiagnosticsConfigPage(ConfigPageMixin, DiagnosticsConfigHandler):
    template = "diagnostics/diagnostics.tpl"


class DiagnosticsPlugin(ForisPlugin):
    PLUGIN_NAME = "diagnostics"
    DIRNAME = os.path.dirname(os.path.abspath(__file__))
    PLUGIN_STYLES = [
        "css/screen.css",
    ]

    def __init__(self, app):
        super(DiagnosticsPlugin, self).__init__(app)
        add_config_page("diagnostics", DiagnosticsConfigPage, top_level=True)
