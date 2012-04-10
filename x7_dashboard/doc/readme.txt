###########################################################
# x7tools and dashboard intergrade
openstack-dashboard/setting.py

1) add x7tools to INSTALLED_APPS
INSTALLED_APPS{
    ...
    'x7tools',
}
openstack-dashboard/local/local_settings.py
1) add tools to HORIZON_CONFIG
HORIZON_CONFIG = {
    'dashboards': ('nova', 'syspanel', 'settings','tools',),
    ...
}

#########################################################################
#use djange db cache:
cd horizon/openstack-dashboard
python manage.py createcachetable x7_cache_table


openstack-dashboard/setting.py
#add or change CACHE_BACKEND
LIVE_SERVER_PORT = 8000
CACHE_BACKEND = 'db://x7_cache_table?timeout=3000&max_entries=400'

MIDDLEWARE_CLASSES:
    'django.middleware.cache.CacheMiddleware',
    


