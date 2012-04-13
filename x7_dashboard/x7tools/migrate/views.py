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

"""
Views for managing Engine instances.
"""
import datetime
import simplejson
import logging

from django import http
from django import shortcuts
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext as _
#import x7x.api.exceptions as api_exceptions
from x7tools.x7_mq import MqClient,MqReader
from horizon.api.base import *
import simplejson

import horizon
from nova_cmd import host_vm_list

from django.core.cache import cache


template_name = 'x7tools/migrate/index.html'

def get_data( request):
        return shortcuts.render(request, template_name, {}, content_type="text/html")

@login_required
def migrate(request):
    return get_data( request )

@login_required
def get_x7data(request):
    #todo  
    #json = [{'instances': [{'node': 'spring', 'kernel': '4e13a156-a959-44d9-b312-32183a2a3f28', 'ramdisk': '', 'image': '2653d13d-0611-4d8f-ad52-6ab64ba3d672', 'user': 'admin', 'index': '1', 'zone': 'None', 'project': '22f4e387e60543a7822f8476c359ce58', 'instance': 'Ubuntu-Server', 'state': 'error', 'type': 'm1.tiny', 'launched': 'None'},{'node': 'spring', 'kernel': '4e13a156-a959-44d9-b312-32183a2a3f28', 'ramdisk': '', 'image': '2653d13d-0611-4d8f-ad52-6ab64ba3d672', 'user': 'admin', 'index': '2', 'zone': 'None', 'project': '22f4e387e60543a7822f8476c359ce58', 'instance': 'i0000001', 'state': 'error', 'type': 'm1.tiny', 'launched': 'None'}], 'host': 'spring', 'zone': 'nova'},{'instances': [{'node': 'host106', 'kernel': '4e13a156-a959-44d9-b312-32183a2a3f28', 'ramdisk': '', 'image': '2653d13d-0611-4d8f-ad52-6ab64ba3d672', 'user': 'admin', 'index': '1', 'zone': 'None', 'project': '22f4e387e60543a7822f8476c359ce58', 'instance': 'i0000003', 'state': 'error', 'type': 'm1.tiny', 'launched': 'None'}], 'host': 'host106', 'zone': 'nova'},]
    json = host_vm_list()    
    
    print json
        
    return shortcuts.render(request, 'x7tools/ajax.html', {"json":json}, content_type="text/html")

def submit_migrate(request):        
    data = {}
    data['instance'] = request.POST['instance']
    #data['host'] = request.POST['host']
    data['host'] = " "
    data['type'] = "cmd"
    data['mesg'] = "migrate"
    
    
    mw2sDict = { 'X7_Q':'X7_Q_MW2S', 'X7_E':'X7_E_MW2S', 'X7_RK':'X7_PK_MW2S' }
    client = MqClient( mw2sDict )
    client.connect()
    client.send( simplejson.dumps( data )  )      
    
    #save begin migrate status
    cache.set('migrate_'+data['instance'], 'running', 3000 );
    cache.set('migrate_'+data['instance']+ "_desc", 'running', 3000 );
    
    return shortcuts.render(request, 'x7tools/migrate/query.html', {"json": data }, content_type="text/html")

def query_migrate(request):   
    instance = None
    if 'instance' in request.GET:
        instance  = request.GET['instance']
    else:
        return shortcuts.render(request, 'x7tools/ajax.html', {"json":{"mesg":"error", "desc":"query migrate status need instance param"}}, content_type="text/html")

    ms2wDict = { 'X7_Q':'X7_Q_MS2W', 'X7_E':'X7_E_MS2W', 'X7_RK':'X7_PK_MS2W' }
    reader = MqReader( ms2wDict )
    reader.connect()
    
    mesg = reader.get()
    pkg = {}
    if mesg is not None:
        pkg = mesg.payload;
        
        #save begin migrate result
        cache.set('migrate_'+pkg['instance'], pkg['mesg'], 3000 );
        cache.set('migrate_'+pkg['instance']+'_desc', pkg['desc'], 3000 );
    else:
        #read from cache
        mesg = cache.get('migrate_'+instance )
        desc = cache.get('migrate_'+instance + "_desc")
        pkg['mesg'] = mesg
        pkg['desc'] = desc        
  
    json = simplejson.dumps( pkg )
    #print json

    return shortcuts.render(request, 'x7tools/ajax.html', {"json":json}, content_type="text/html")
    
    









