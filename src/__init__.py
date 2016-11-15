# Foris - web administration interface for OpenWrt based on NETCONF
# Copyright (C) 2016 CZ.NIC, z. s. p. o. <https://www.nic.cz>
#
# Foris is distributed under the terms of GNU General Public License v3.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import bottle
import os


from foris.core import gettext_dummy as gettext, ugettext as _
from foris.config import ConfigPageMixin, add_config_page
from foris.config_handlers import BaseConfigHandler
from foris.plugins import ForisPlugin
from foris.utils import messages
from foris.utils.routing import reverse

from .nuci import get_diagnostics, get_diagnostics_modules, get_diagnostic, remove_diagnostic


class DiagnosticsConfigHandler(BaseConfigHandler):
    pass


class DiagnosticsConfigPage(ConfigPageMixin, DiagnosticsConfigHandler):
    template = "diagnostics/diagnostics.tpl"
    userfriendly_title = gettext("Diagnostics")

    DIAGNOSTIC_STATUS_TRANSLATION = {
        'missing': gettext("Missing"),
        'preparing': gettext("Preparing"),
        'ready': gettext("Ready"),
        'unknown': gettext("Unknown"),
    }

    @staticmethod
    def translate_diagnostic_status(status):
        res = _(DiagnosticsConfigPage.DIAGNOSTIC_STATUS_TRANSLATION.get(
            status,
            DiagnosticsConfigPage.DIAGNOSTIC_STATUS_TRANSLATION['unknown'],
        ))
        return res

    def _action_download_diagnostic(self):
        diag_id = bottle.request.POST.get("id")
        output = get_diagnostic(diag_id).output

        if not output:
            messages.error(_("Unable to get diagnostic \"%s\".") % diag_id)
            bottle.redirect(reverse("config_page", page_name="diagnostics"))
        else:
            bottle.response.set_header("Content-Type", "text/plain")
            bottle.response.set_header(
                "Content-Disposition", 'attachment; filename="%s.txt.gz' % diag_id)
            bottle.response.set_header("Content-Length", len(output))
            return output

    def _action_remove_diagnostic(self):
        diag_id = bottle.request.POST.get("id")

        if remove_diagnostic(diag_id):
            messages.success(_("Diagnostic \"%s\" removed.") % diag_id)
        else:
            messages.error(_("Unable to remove diagnostic \"%s\".") % diag_id)

        bottle.redirect(reverse("config_page", page_name="diagnostics"))

    def call_action(self, action):
        if bottle.request.method != 'POST':
            # all actions here require POST
            messages.error("Wrong HTTP method.")
            bottle.redirect(reverse("config_page", page_name="diagnostics"))
        if action == "download":
            return self._action_download_diagnostic()
        elif action == "remove":
            return self._action_remove_diagnostic()
        raise bottle.HTTPError(404, "Unknown action.")

    def render(self, **kwargs):
        kwargs['PLUGIN_NAME'] = DiagnosticsPlugin.PLUGIN_NAME
        kwargs['PLUGIN_STYLES'] = DiagnosticsPlugin.PLUGIN_STYLES

        kwargs['modules'] = get_diagnostics_modules().module_list
        kwargs['diagnostics'] = get_diagnostics().list
        kwargs['translate_diagnostic_status'] = self.translate_diagnostic_status

        return super(DiagnosticsConfigPage, self).render(**kwargs)


class DiagnosticsPlugin(ForisPlugin):
    PLUGIN_NAME = "diagnostics"
    DIRNAME = os.path.dirname(os.path.abspath(__file__))
    PLUGIN_STYLES = [
        "css/screen.css",
    ]

    def __init__(self, app):
        super(DiagnosticsPlugin, self).__init__(app)
        add_config_page("diagnostics", DiagnosticsConfigPage, top_level=True)
