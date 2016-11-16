%# Foris - web administration interface for OpenWrt based on NETCONF
%# Copyright (C) 2016 CZ.NIC, z. s. p. o. <https://www.nic.cz>
%#
%# Foris is distributed under the terms of GNU General Public License v3.
%# You should have received a copy of the GNU General Public License
%# along with this program.  If not, see <https://www.gnu.org/licenses/>.

%rebase("config/base.tpl", **locals())

<div id="page-plugin-diagnostics" class="config-page">
    %include("_messages.tpl")
    <p>{{ description }}</p>
    <h2>{{ trans("Prepare diagnostics") }}</h2>
    <form method='post' action='{{ url("config_action", page_name="diagnostics", action="prepare") }}'>
        <input type="hidden" name="csrf_token" value="{{ get_csrf_token() }}">
        %for section in form.sections:
            %if section.active_fields:
                %for field in section.active_fields:
                    %include("_field.tpl", field=field)
                %end
            %end
        %end
        <br />
        <button name="prepare" type="submit">{{ trans("Generate") }}</button>
    </form>
    %if diagnostics:
    <h2>{{ trans("List diagnostics") }}</h2>
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
                    %if diagnostic.status == "ready":
                    <form method='post' action="{{ url("config_action", page_name="diagnostics", action="remove") }}">
                        <input type="hidden" name="csrf_token" value="{{ get_csrf_token() }}">
                        <button name="id" value="{{ diagnostic.diag_id }}" type="submit">{{ trans("Remove") }}
                    </form>
                    %end
                </td>
            </tr>
            %end
        </tbody>
    </table>
    %end
</div>
