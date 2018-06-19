# Foris - web administration interface for OpenWrt based on NETCONF
# Copyright (C) 2017 CZ.NIC, z. s. p. o. <https://www.nic.cz>
#
# Foris is distributed under the terms of GNU General Public License v3.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import bottle
import io
import os
import re
import gzip


from foris import fapi
from foris.utils.translators import gettext_dummy as gettext, ugettext as _
from foris.config import ConfigPageMixin, add_config_page
from foris.config_handlers import BaseConfigHandler
from foris.form import Checkbox
from foris.plugins import ForisPlugin
from foris.utils import messages
from foris.utils.routing import reverse

from foris.state import current_state


class DiagnosticsConfigHandler(BaseConfigHandler):
    userfriendly_title = gettext("Diagnostics")

    def get_form(self):
        modules_form = fapi.ForisForm("modules", self.data)
        modules_section = modules_form.add_section(name="modules", title=_("Modules"))
        data = current_state.backend.perform("diagnostics", "list_modules")
        for module in data["modules"]:
            modules_section.add_field(
                Checkbox, name="module_%s" % module, label=module, default=True,
            )

        return modules_form


class DiagnosticsConfigPage(ConfigPageMixin, DiagnosticsConfigHandler):
    menu_order = 90
    template = "diagnostics/diagnostics.tpl"

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

        def _error_redirect():
            messages.error(_("Unable to get diagnostic \"%s\".") % diag_id)
            bottle.redirect(reverse("config_page", page_name="diagnostics"))

        if not re.match(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}_[a-zA-Z0-9]{8}$', diag_id):
            _error_redirect()
            return

        try:
            data = current_state.backend.perform("diagnostics", "list_diagnostics")
            diagnostics = [e for e in data["diagnostics"] if e["diag_id"] == diag_id]
            filename = '%s.txt.gz' % diag_id
            if len(diagnostics) != 1:
                _error_redirect()
                return
            with open(diagnostics[0]["path"]) as f_in:
                buf = io.BytesIO()
                f_out = gzip.GzipFile(filename=filename, mode="wb", fileobj=buf)
                f_out.write(f_in.read())
                f_out.flush()
                f_out.close()
                buf.seek(0)
                output = buf.read()
        except IOError:
            _error_redirect()
            return

        bottle.response.set_header("Content-Type", "text/plain")
        bottle.response.set_header(
            "Content-Disposition", 'attachment; filename="%s"' % filename)
        bottle.response.set_header("Content-Length", len(output))
        return output

    def _action_remove_diagnostic(self):
        diag_id = bottle.request.POST.get("id")

        data = current_state.backend.perform(
            "diagnostics", "remove_diagnostic", {"diag_id": diag_id})
        if data["result"]:
            messages.success(_("Diagnostic \"%s\" removed.") % diag_id)
        else:
            messages.error(_("Unable to remove diagnostic \"%s\".") % diag_id)

        bottle.redirect(reverse("config_page", page_name="diagnostics"))

    def _action_prepare_diagnostic(self):
        modules = [
            k.replace("module_", "", 1) for k, v in bottle.request.POST.allitems()
            if v == "1" and k.startswith("module_")
        ]

        data = current_state.backend.perform(
            "diagnostics", "prepare_diagnostic", {"modules": modules})
        if "diag_id" in data:
            messages.success(_("Diagnostic \"%s\" is being prepared.") % data["diag_id"])
        else:
            messages.error(_("Failed to generate diagnostic."))

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
        elif action == "prepare":
            return self._action_prepare_diagnostic()
        raise bottle.HTTPError(404, "Unknown action.")

    def render(self, **kwargs):
        kwargs['PLUGIN_NAME'] = DiagnosticsPlugin.PLUGIN_NAME
        kwargs['PLUGIN_STYLES'] = DiagnosticsPlugin.PLUGIN_STYLES

        data = current_state.backend.perform("diagnostics", "list_diagnostics")
        kwargs['diagnostics'] = data["diagnostics"]
        kwargs['translate_diagnostic_status'] = self.translate_diagnostic_status
        kwargs['form'] = self.form
        kwargs['title'] = self.userfriendly_title
        kwargs['description'] = _(
            "This page is dedicated to create diagnotics which can be useful to us to "
            "debug some problems related to the router's functionality. "
        )

        return self.default_template(**kwargs)


class DiagnosticsPlugin(ForisPlugin):
    PLUGIN_NAME = "diagnostics"
    DIRNAME = os.path.dirname(os.path.abspath(__file__))
    PLUGIN_STYLES = [
        "css/diagnostics.css",
    ]

    def __init__(self, app):
        super(DiagnosticsPlugin, self).__init__(app)
        add_config_page("diagnostics", DiagnosticsConfigPage, top_level=True)
