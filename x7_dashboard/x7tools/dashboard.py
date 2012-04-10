# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.utils.translation import ugettext as _

import horizon


class X7ToolsPanels(horizon.PanelGroup):
    slug = "tools"
    name = _("Tools Panel")
    panels = ('setup', 'migrate',)
    
class X7Tools(horizon.Dashboard):
    name = "Tools"
    slug = "tools"
#    panels = {_("X7Tools"): ('setup', 'migrate',),  }
    panels = (X7ToolsPanels,)
    default_panel = 'setup'
    roles = ('admin',)

horizon.register(X7Tools)
