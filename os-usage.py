#!/usr/bin/env python

import json, subprocess

def run_cmd(cmd):
    text = subprocess.check_output((cmd + ' --format json').split(), universal_newlines=True)
    data = json.loads(text)
    return data

hv_list = run_cmd('openstack hypervisor list')
print('got data for %i hypervisors' % len(hv_list))
baremetal = {'total':0, 'busy':0, 'free':0}

for hv in hv_list:
    hv_data = run_cmd('openstack hypervisor show %s' % hv['ID'])
    if hv['Hypervisor Type'] == 'QEMU':
        print(hv_data)
        exit()
    elif hv['Hypervisor Type'] == 'ironic':
        baremetal['total'] += 1
        if int(hv_data['running_vms']) > 0:
            baremetal['busy'] += 1
        else:
            baremetal['free'] += 1

print('baremetal:', baremetal)
