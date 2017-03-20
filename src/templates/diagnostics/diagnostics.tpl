%# Foris - web administration interface for OpenWrt based on NETCONF
%# Copyright (C) 2017 CZ.NIC, z. s. p. o. <https://www.nic.cz>
%#
%# Foris is distributed under the terms of GNU General Public License v3.
%# You should have received a copy of the GNU General Public License
%# along with this program.  If not, see <https://www.gnu.org/licenses/>.

%rebase("config/base.tpl", **locals())

<div id="page-plugin-diagnostics" class="config-page">
    %include("_messages.tpl")
    <p>{{ description }}</p>
    <h2>{{ trans("Modules") }}</h2>
    <form method='post' action='{{ url("config_action", page_name="diagnostics", action="prepare") }}'>
        <input type="hidden" name="csrf_token" value="{{ get_csrf_token() }}">
        <table>
            <tbody>
        %for section in form.sections:
            %if section.active_fields:
                %for field in section.active_fields:
                    <tr>
                        <td>
                            {{! field.render() }}
                            %if field.errors:
                              <div class="server-validation-container">
                                <ul>
                                  <li>{{ field.errors }}</li>
                                </ul>
                              </div>
                            %end
                        </td>
                        <td>
                            {{! field.label_tag }}
                            %if field.hint:
                                <img class="field-hint" src="{{ static("img/icon-help.png") }}" title="{{ field.hint }}" alt="{{ trans("Hint") }}: {{ field.hint }}">
                            %end
                        </td>
                    </tr>
                %end
            %end
        %end
            </tbody>
        </table>
        <br />
        <button name="prepare" type="submit">{{ trans("Generate") }}</button>
    </form>
    %if diagnostics:
    <h2>{{ trans("List") }}</h2>
    <p><strong>{{ trans("Some of the diagnostics might contain a sensitive data so make sure to remove it before sharing.") }}</strong></p>
    <table class='diagnostics-list'>
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
                    <table>
                        <tbody>
                            <tr>
                                <td>
                                    <form method='post' action="{{ url("config_action", page_name="diagnostics", action="download") }}">
                                        <input type="hidden" name="csrf_token" value="{{ get_csrf_token() }}">
                                        <button name="id" value="{{ diagnostic.diag_id }}" type="submit">{{ trans("Download") }}
                                    </form>
                                </td>
                                <td>
                                    <form method='post' action="{{ url("config_action", page_name="diagnostics", action="remove") }}">
                                        <input type="hidden" name="csrf_token" value="{{ get_csrf_token() }}">
                                        <button name="id" value="{{ diagnostic.diag_id }}" type="submit">{{ trans("Remove") }}
                                    </form>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    %end
                </td>
            </tr>
            %end
        </tbody>
    </table>
    <br />
    <p>{{ trans("Note that this list is not presistent and will be removed after reboot.") }}</p>
    %end
</div>
