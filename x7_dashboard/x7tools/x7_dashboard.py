# vim: tabstop=4 shiftwidth=4 softtabstop=4

import logging
from horizon.api.base import *

LOG = logging.getLogger(__name__)


def x7tools_api(request):
    management_url = url_for(request, 'x7tools')
    LOG.debug('x7tools connection created using token "%s"'
                     ' and url "%s"' %
                    (request.user.token, management_url))
#
#

def x7tools_query(request, **kwargs):
    return x7tools_api(request).query(**kwargs)
