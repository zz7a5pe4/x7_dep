# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
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


from django.conf.urls.defaults import *


urlpatterns = patterns('x7tools',
    url(r'^get_hostlist$', 'setup.views.get_hostlist', name='get_hostlist'),
    url(r'^submit_setup$', 'setup.views.submit_setup', name='submit_setup'),
    url(r'^query_setup$', 'setup.views.query_setup', name='query_setup'),
    url(r'^$', 'setup.views.setup', name='index'),
)
