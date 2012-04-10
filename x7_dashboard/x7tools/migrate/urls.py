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
    url(r'^get_x7data$', 'migrate.views.get_x7data', name='get_x7data'),
    url(r'^submit_migrate$', 'migrate.views.submit_migrate', name='submit_migrate'),
    url(r'^query_migrate$', 'migrate.views.query_migrate', name='query_migrate'),
    url(r'^get_x7data$', 'migrate.views.get_x7data', name='get_x7data'),    
    url(r'^$', 'migrate.views.migrate', name='index'),
)
