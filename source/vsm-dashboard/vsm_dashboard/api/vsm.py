# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
# Copyright 2014 Intel Corporation, All Rights Reserved.
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

from __future__ import absolute_import

import logging
from vsmclient.v1 import client as vsm_client
from vsmclient.v1.pool_usages import PoolUsageManager
from vsmclient.v1.appnodes import AppNodeManager
from vsm_dashboard.api.base import APIResourceWrapper
from django.conf import settings

LOG = logging.getLogger(__name__)

class ExtensionManager:
    def __init__(self, name, manager_class):
        self.name = name
        self.manager_class = manager_class

def vsmclient(request):
    key_vsm_pass = getattr(settings,'KEYSTONE_VSM_SERVICE_PASSWORD')
    key_url = getattr(settings, 'OPENSTACK_KEYSTONE_URL')
    c = vsm_client.Client('vsm',
                          key_vsm_pass,
                          'service',
                          key_url,
                          extensions=[ExtensionManager('PoolUsageManager',
                                                PoolUsageManager),
                                      ExtensionManager('AppNodeManager',
                                                AppNodeManager)])
    return c

class Pool(APIResourceWrapper):
    """Simple wrapper around vsmclient.vsms
    """
    _attrs = ['id', 'name', 'status', 'recipe_id', 'deleted']

    def __init__(self, apiresource, request):
        super(Pool, self).__init__(apiresource)
        self.request = request

def create_storage_pool(request, body):
    return vsmclient(request).vsms.create_storage_pool(body)

def add_cache_tier(request, body):
    return vsmclient(request).storage_pools.add_cache_tier(body)

def remove_cache_tier(request, body):
    return vsmclient(request).storage_pools.remove_cache_tier(body)

def get_storage_group_list(request):
    return vsmclient(request).vsms.get_storage_group_list()

def get_pool_size_list(request):
    return vsmclient(request).vsms.get_pool_size_list()

def pools_list(request, search_opts=None, all_pools=False):
    if search_opts is None:
        search_opts = {}
    if all_pools:
        search_opts['all_pools'] = True
    return vsmclient(request).vsms.list_storage_pool(request, search_opts)

def pool_list(request):
    search_opts = {}
    r, pool_list = vsmclient(request).vsms.list_storage_pool(request, search_opts)
    return pool_list['pool']

def pool_usages(request):
    return vsmclient(request).PoolUsageManager.list()

def present_pool(request, pools):
    return vsmclient(request).PoolUsageManager.create(pools=pools)

def add_appnodes(request, ips):
    return vsmclient(request).AppNodeManager.create(ips=ips)

def del_appnode(request, appnode_id):
    return vsmclient(request).AppNodeManager.delete(appnode_id)

def update_appnode(request, appnode, **kwargs):
    return vsmclient(request).AppNodeManager.update(appnode, **kwargs)

def appnode_list(request,):
    return vsmclient(request).AppNodeManager.list()

resp = None
#server api
def add_servers(request, servers=[]):
    return vsmclient(request).servers.add(servers)

def remove_servers(request, servers=[]):
    return vsmclient(request).servers.remove(servers)

def reset_status(request, servers):
    return vsmclient(request).servers.reset_status(servers)

def get_server_list(request):
    return vsmclient(request).servers.list()

def get_server(request, id):
    return vsmclient(request).servers.get(id)

def start_server(request, servers=None):
    """Start servers.
       servers = [{'id': 1}, {'id': 2}]
    """
    return vsmclient(request).servers.start(servers)

def stop_server(request, servers=None):
    """Stop servers.
       servers = [{'id': 1}, {'id': 2}]
    """
    LOG.debug("DEBUG in stop server of dashboard api")
    return vsmclient(request).servers.stop(servers)

#zone api
def get_zone_list(request):
    return vsmclient(request).zones.list()

# TODO return the exact response
def create_zone(request, opts=None):
    res = vsmclient(request).zones.create(opts)
    return resp, {'status': "succes", "message": "create zone success"}

#cluster api
def get_cluster_list(request, opts=None):
    return vsmclient(request).vsms.get_cluster_list()

def create_cluster(request, servers=[]):
    return vsmclient(request).clusters.create(servers=servers)

def intergrate_cluster(request, servers=[]):
    return vsmclient(request).clusters.intergrate(servers=servers)
#osd api
def osd_list(request):
    return vsmclient(request).osds.list()

def osd_get(request, osd_id):
    return vsmclient(request).osds.get(osd_id)

def osd_restart(request, osd_id):
    return vsmclient(request).osds.restart(osd_id)

def osd_delete(request, osd_id):
    return vsmclient(request).osds.delete(osd_id)

def osd_remove(request, osd_id):
    return vsmclient(request).osds.remove(osd_id)

def osd_restore(request, osd_id):
    return vsmclient(request).osds.restore(osd_id)

def osd_status(request, paginate_opts=None):
    return vsmclient(request).osds.list(detailed=True, paginate_opts=paginate_opts)

def osd_summary(request):
    return vsmclient(request).osds.summary()

def mds_status(request):
    return vsmclient(request).mdses.list(detailed=True)

def monitor_summary(request):
    return vsmclient(request).monitors.summary()

def monitor_status(request):
    return vsmclient(request).monitors.list(detailed=True)

def storage_group_summary(request):
    return vsmclient(request).storage_groups.summary()

def storage_group_status(request):
    return vsmclient(request).storage_groups.list(detailed=True)

def storage_group_create(request, body):
    return vsmclient(request).storage_groups.create(body)

def placement_group_summary(request):
    return vsmclient(request).placement_groups.summary()

def placement_group_status(request, paginate_opts=None):
    return vsmclient(request).placement_groups.list(detailed=True,
                                                    paginate_opts=paginate_opts)

def rbd_pool_summary(request):
    return vsmclient(request).rbd_pools.summary()

def rbd_pool_status(request, paginate_opts=None):
    return vsmclient(request).rbd_pools.list(detailed=True, paginate_opts=paginate_opts)

def mds_summary(request):
    return vsmclient(request).mdses.summary()

def cluster_summary(request):
    return vsmclient(request).clusters.summary()

def vsm_summary(request):
    return vsmclient(request).vsms.summary()

def pool_status(request):
    return vsmclient(request).storage_pools.list(detailed=True)

def ec_profiles(request):
    return vsmclient(request).storage_pools.ec_profiles()

#device api
def device_list(request):
    return vsmclient(request).devices.list()

#license api
def license_create(request, value=True):
    return vsmclient(request).licenses.license_create(value)

def license_get(request):
    return vsmclient(request).licenses.license_get()

def license_update(request, value):
    return vsmclient(request).licenses.license_update(value)

def get_setting_dict(request,):
    # TODO
    setting_list = vsmclient(request).vsm_settings.list()
    setting_dict = {}
    for setting in setting_list:
        setting_dict.setdefault(setting.name, setting.value)
    return setting_dict

def get_settings(request,):
    return vsmclient(request).vsm_settings.list()

def get_setting_by_name(request, name):
    return vsmclient(request).vsm_settings.get(name)

def update_setting(request, name, value):
    return vsmclient(request).vsm_settings.create({'name': name, 'value':value})

