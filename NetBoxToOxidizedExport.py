from NetBoxPython import NetBoxPython as NetBoxPython
from datetime import datetime

BASE_API_URL = 'http://site.ru/api/'
API_HEADERS = {
        'Authorization': 'Token *****',
        'Accept': 'application/json',
        'Content-Type': 'application/json'}

ITEM_GROUP = 'dcim'
ITEM_TYPE = 'devices'
INVENTORY_FILE = '/opt/oxidized/inventory'
HOSTS_FILE = '/etc/hosts'
LOG_FILE = '/var/log/NetBoxToOxidizedExport.log'


def delete_items_with_exceptions(log_file_path):
    for item in netbox_to_oxidized.items_list[:]:
        try:
            if item['device_role']['slug'] in ['km-ups', 'dc-fex', 'km-hv', 'km-wf-ap']:
                with open(log_file_path, 'a') as log_file:
                    log_file.write('{} INFO: {} will not be processed because has inappropriate device role ({})\n'.format(
                            now.strftime('%Y-%m-%d %H:%M'),
                            item['name'], item['device_role']['slug']))
                log_file.close()
                netbox_to_oxidized.items_list.remove(item)
            elif item['status']['label'] != 'Active':
                with open(log_file_path, 'a') as log_file:
                    log_file.write('{} INFO: {} will not be processed because not in active state\n'.format(
                            now.strftime('%Y-%m-%d %H:%M'),
                            item['name']))
                log_file.close()
                netbox_to_oxidized.items_list.remove(item)
            elif item['custom_fields']['Web Only']:
                with open(log_file_path, 'a') as log_file:
                    log_file.write(
                        '{} INFO: {} will not be processed because accessible only via web interface ({} {})\n'.format(
                            now.strftime('%Y-%m-%d %H:%M'),
                            item['name'], item['device_type']['manufacturer']['name'],
                            item['device_type']['model']))
                log_file.close()
                netbox_to_oxidized.items_list.remove(item)
            elif item['custom_fields']['Authorization Type']['label'] == 'Local Credentials':
                with open(log_file_path, 'a') as log_file:
                    log_file.write(
                        '{} INFO: {} will not be processed because has only local credentials ({} {})\n'.format(
                            now.strftime('%Y-%m-%d %H:%M'),
                            item['name'], item['device_type']['manufacturer']['name'],
                            item['device_type']['model']))
                log_file.close()
                netbox_to_oxidized.items_list.remove(item)
        except TypeError:
            pass


def form_output_inventory(inventory_file_path, log_file_path):
    with open(inventory_file_path, 'w') as inventory_file:
        for item in netbox_to_oxidized.items_list:
            try:
                if item['device_role']['slug'] == 'km-asw':
                    inventory_file.write('{}:{}:lan/{}/{}\n'.format(item['name'], item['platform']['slug'],
                                                                    item['device_role']['slug'], item['site']['slug']).lower())
                else:
                    inventory_file.write('{}:{}:lan/{}\n'.format(item['name'], item['platform']['slug'],
                                                                 item['device_role']['slug']).lower())
            except:
                with open(log_file_path, 'a') as log_file:
                    log_file.write('{} WARN: {} does not have some values (inventory file)\n'.format(now.strftime('%Y-%m-%d %H:%M'), item['name']))
                log_file.close()
        inventory_file.close()


def form_output_hosts(hosts_file_path, log_file_path):
    with open(hosts_file_path, 'w') as hosts_file:
        for item in netbox_to_oxidized.items_list:
            try:
                hosts_file.write('{}     {}\n'.format(item['primary_ip']['address'].split('/')[0], item['name'].lower()))
            except:
                with open(log_file_path, 'a') as log_file:
                    log_file.write('{} WARN: {} does not have some values (hosts file)\n'.format(now.strftime('%Y-%m-%d %H:%M'), item['name']))
                log_file.close()
        hosts_file.close()


if __name__ == "__main__":
    now = datetime.now()

    with open(LOG_FILE, 'a') as log_file:
        log_file.write('{} START EXECUTION\n'.format(now.strftime('%Y-%m-%d %H:%M')))
    log_file.close()

    netbox_to_oxidized = NetBoxPython(BASE_API_URL, API_HEADERS, ITEM_GROUP, ITEM_TYPE)
    netbox_to_oxidized.form_request_string()
    netbox_to_oxidized.get_all_items()

    delete_items_with_exceptions(LOG_FILE)
    form_output_inventory(INVENTORY_FILE, LOG_FILE)
    form_output_hosts(HOSTS_FILE, LOG_FILE)
