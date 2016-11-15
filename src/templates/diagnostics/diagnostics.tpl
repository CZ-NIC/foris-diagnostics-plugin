%# Foris - web administration interface for OpenWrt based on NETCONF
%# Copyright (C) 2016 CZ.NIC, z. s. p. o. <https://www.nic.cz>
%#
%# Foris is distributed under the terms of GNU General Public License v3.
%# You should have received a copy of the GNU General Public License
%# along with this program.  If not, see <https://www.gnu.org/licenses/>.

%rebase("config/base.tpl", **locals())

<div id="page-plugin-diagnostics" class="config-page">
    %include("_messages.tpl")
    <h2>{{ trans("Available modules") }}</h2>
    <ul>
        %for module in modules:
        <li>{{ module }}</li>
        %end
    </ul>
    <h2>{{ trans("Prepared diagnostics") }}</h2>
    <table>
        <thead>
            <tr>
                <th>{{ trans("ID") }}</th>
                <th>{{ trans("status") }}</th>
                <th></th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            %for diagnostic in diagnostics:
            <tr>
                <td>{{ diagnostic.diag_id }}</td>
                <td>{{ translate_diagnostic_status(diagnostic.status) }}</td>
                <td>
                    %if diagnostic.status == "ready":
                    <form method='post' action="{{ url("config_action", page_name="diagnostics", action="download") }}">
                        <input type="hidden" name="csrf_token" value="{{ get_csrf_token() }}">
                        <button name="id" value="{{ diagnostic.diag_id }}" type="submit">{{ trans("Download") }}
                    </form>
                    %end
                </td>
                <td>
                    <form method='post' action="{{ url("config_action", page_name="diagnostics", action="remove") }}">
                        <input type="hidden" name="csrf_token" value="{{ get_csrf_token() }}">
                        <button name="id" value="{{ diagnostic.diag_id }}" type="submit">{{ trans("Remove") }}
                    </form>
                </td>
            </tr>
            %end
        </tbody>
    </table>
</div>
