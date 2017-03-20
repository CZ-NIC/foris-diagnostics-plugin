# Foris - web administration interface for OpenWrt based on NETCONF
# Copyright (C) 2017 CZ.NIC, z. s. p. o. <https://www.nic.cz>
#
# Foris is distributed under the terms of GNU General Public License v3.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import base64

from xml.etree import cElementTree as ET

from foris.nuci.modules.base import YinElement

DIAGNOSTICS_URI = "http://www.nic.cz/ns/router/diagnostics"


class Modules(YinElement):
    tag = "list-modules"
    NS_URI = DIAGNOSTICS_URI

    def __init__(self, module_list):
        super(Modules, self).__init__()
        self.module_list = module_list

    @staticmethod
    def from_element(element):
        diagnostics_node = element.find(Modules.qual_tag("diagnostics"))
        module_nodes = diagnostics_node.findall(Modules.qual_tag("module"))
        module_list = [e.text for e in module_nodes]
        return Modules(module_list)

    @staticmethod
    def rpc_list_modules():
        get_tag = Modules.qual_tag(Modules.tag)
        return ET.Element(get_tag)

    @property
    def key(self):
        return "list-modules"

    def __str__(self):
        return "Diagnostics Modules"


class List(YinElement):
    tag = "list-diagnostics"
    NS_URI = DIAGNOSTICS_URI

    def __init__(self, diag_list):
        super(List, self).__init__()
        self.list = diag_list

    @staticmethod
    def from_element(element):
        diagnostics_node = element.find(Modules.qual_tag("diagnostics"))
        diagnostic_nodes = diagnostics_node.findall(Modules.qual_tag("diagnostic"))
        diagnostics_list = []
        for diagnostic in diagnostic_nodes:
            diagnostics_list.append(ListItem.from_element(diagnostic))
        return List(diagnostics_list)

    @staticmethod
    def rpc_list_diagnostics():
        get_tag = List.qual_tag(List.tag)
        return ET.Element(get_tag)

    @property
    def key(self):
        return "list-modules"

    def __str__(self):
        return "Diagnostics List"


class ListItem(object):

    def __init__(self, diag_id, status):
        self.diag_id = diag_id
        self.status = status

    @staticmethod
    def from_element(element):
        diag_id = element.find(List.qual_tag("diag-id")).text
        status = element.find(List.qual_tag("status")).text
        return ListItem(diag_id, status)


class Show(YinElement):
    tag = "get-prepared"
    NS_URI = DIAGNOSTICS_URI

    def __init__(self, output):
        super(Show, self).__init__()
        self.output = output

    @staticmethod
    def rpc_get(diag_id):
        get_tag = Show.qual_tag(Show.tag)

        element = ET.Element(get_tag)
        id_tag = Show.qual_tag("diag-id")
        id_elem = ET.SubElement(element, id_tag)
        id_elem.text = diag_id

        return element

    @staticmethod
    def from_element(element):
        diagnostics_node = element.find(Show.qual_tag("diagnostics"))
        status = diagnostics_node.find(Show.qual_tag("status")).text
        if status == "ready":
            output = base64.decodestring(diagnostics_node.find(Show.qual_tag("output")).text)
        else:
            output = None

        return Show(output)


class Remove(YinElement):
    tag = "remove-diagnostic"
    NS_URI = DIAGNOSTICS_URI

    def __init__(self, result):
        super(Remove, self).__init__()
        self.result = result

    @staticmethod
    def rpc_remove(diag_id):
        remove_tag = Remove.qual_tag(Remove.tag)

        element = ET.Element(remove_tag)
        id_tag = Remove.qual_tag("diag-id")
        id_elem = ET.SubElement(element, id_tag)
        id_elem.text = diag_id

        return element


class Prepare(YinElement):
    tag = "prepare"
    NS_URI = DIAGNOSTICS_URI

    def __init__(self, diag_id):
        super(Prepare, self).__init__()
        self.diag_id = diag_id

    @staticmethod
    def rpc_prepare(modules):
        prepare_tag = Prepare.qual_tag(Prepare.tag)
        element = ET.Element(prepare_tag)

        for module in modules:
            module_tag = Remove.qual_tag("module")
            module_elem = ET.SubElement(element, module_tag)
            module_elem.text = module

        return element

    @staticmethod
    def from_element(element):
        diagnostics_node = element.find(Show.qual_tag("diagnostics"))
        diag_id = diagnostics_node.find(Show.qual_tag("diag-id")).text
        return Prepare(diag_id)

####################################################################################################
ET.register_namespace("diagnostics", DIAGNOSTICS_URI)
