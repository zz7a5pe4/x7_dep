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

#-*- coding: utf-8 -*-

"""
Views for managing Engine instances.
"""
import datetime
import logging

from django import http
from django import shortcuts
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext as _

from horizon.api.base import *

import horizon
from horizon import api
import urlparse

from x7tools.x7_mq import MqClient,MqReader
import simplejson

template_name = 'x7tools/setup/index.html'

def get_data( request):
    
    hostList = [{"desc":"Host Server 1#","hostname":"cloudnode-1", "status":"waiting"}, \
                {"desc":"Host Server 2#","hostname":"cloudnode-2", "status":"waiting"}, \
                {"desc":"Host Server 3#","hostname":"cloudnode-3", "status":"waiting"} \
               ]
    return hostList


@login_required
#def usage_for_tenant(request, tenant_id=None):
#    return migrate_vm(request, tenant_id or request.user.tenant_id)


@login_required
def setup( request ):   
    return shortcuts.render(request, template_name, {}, content_type="text/html")

@login_required
def get_hostlist( request ):
    hostList = get_data( request );    
    return shortcuts.render(request, "x7tools/ajax.html", {"json":hostList}, content_type="text/html")


@login_required
def submit_setup( request ):
    retHostList = []
    
    host_list = []
    for i in range(0,6):
        if 'check%d' % i in request.POST: 
            a_host={}
            ret_a_host = {}
            hostname = request.POST['hostname%d' % i]
            desc = request.POST['desc%d' % i ]
            
            a_host['hostname'] = hostname
            a_host['desc'] = desc
            
            ret_a_host['hostname'] = hostname
            ret_a_host['desc'] = desc
            ret_a_host['status'] = "running setup"
            
            host_list.append( a_host )
            retHostList.append( ret_a_host )
            
    
    #send request HOST SETUP REQ
    hw2sDict = { 'X7_Q':'X7_Q_HW2S', 'X7_E':'X7_E_HW2S', 'X7_RK':'X7_PK_HW2S' }
    client = MqClient( hw2sDict )
    client.connect()
    client.send( simplejson.dumps( host_list )  )   
    print simplejson.dumps( host_list )
    
    return shortcuts.render(request, "x7tools/setup/query.html", {"json":simplejson.dumps( retHostList )}, content_type="text/html")


@login_required
def query_setup( request ):
    
    hs2wDict = { 'X7_Q':'X7_Q_HS2W', 'X7_E':'X7_E_HS2W', 'X7_RK':'X7_PK_HS2W' }
    reader = MqReader( hs2wDict )
    reader.connect()
    
    dataList = []
    for i in range(1,6):
        mesg = reader.get()
        if mesg is not None:
            dataList.append( mesg.payload )
        else:
            break
    json = simplejson.dumps( dataList )

    #print json

    #[{"type":"cmd", "mesg":"success", "hostname": "cloudnode-1"}, {"type":"log", "mesg":"success", "hostname": "cloudnode-2"}, , {"type":"prog", "mesg":"40", "hostname": "cloudnode-3"}]

    return shortcuts.render(request, 'x7tools/ajax.html', {"json":json}, content_type="text/html")