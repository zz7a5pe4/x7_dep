# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
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

from django.conf import settings
from django.http import HttpResponse
from horizon import usage
import commands


class GlobalOverview(usage.UsageView):
    table_class = usage.GlobalUsageTable
    usage_class = usage.GlobalUsage
    template_name = 'syspanel/overview/usage.html'

    def get_context_data(self, **kwargs):
        context = super(GlobalOverview, self).get_context_data(**kwargs)
        context['monitoring'] = getattr(settings, 'EXTERNAL_MONITORING', [])
        return context

def addhost(request):
    if 'macAddress' in request.GET and request.GET['macAddress']:
        macAddress = request.GET['macAddress']
    else:
        return HttpResponse("Please enter the Mac Address!")

    if 'ipAddress' in request.GET and request.GET['ipAddress']:
        ipAddress =  request.GET['ipAddress']
    else:
        return HttpResponse("Please enter the IP Address!")
    
    cmd = "bash /home/xeven/addhost %s %s" % (macAddress,ipAddress)
    result = commands.getoutput(cmd)
    if "error" in result:
        return HttpResponse("Not Add Host Successfully")
    else:
        return HttpResponse("Succeed in Adding Host")

def installComputeNode(request):
    if 'compIpAddress' in request.GET and request.GET['compIpAddress']:
        compIpAddress = request.GET['compIpAddress']
    else:
        return HttpRespone("Please enter the IP Address")
    
    cmd = "python /home/xeven/comp_setup.py %s" % compIpAddress
    result = commands.getoutput(cmd)
    if "error" in result:
        return HttpResponse("Not Install Compute Node Successfully")
    else:
        return HttpResponse("Succeed in Installing Compute Node")
