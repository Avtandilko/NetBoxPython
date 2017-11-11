import requests
import json


class NetBoxPythonApi:
    def __init__(self, base_api_url, api_headers, item_group, item_type):
        self.base_api_url = base_api_url
        self.api_headers = api_headers
        self.item_group = item_group
        self.item_type = item_type
        self.request_string = ''
        self.all_items = ''
        self.items_list = []
        self.item = ''

    def form_request_string(self):
        self.request_string = ('{}{}/{}'.format(self.base_api_url, self.item_group, self.item_type))
        return self.request_string

    # Type of self.items_list is a list
    def get_all_items(self):
        self.all_items = requests.get(self.request_string, headers=self.api_headers).json()
        for item in self.all_items['results']:
            self.items_list.append(item)
        while self.all_items['next']:
            self.request_string = self.all_items['next']
            self.get_all_items()
        return self.items_list

    # Type of self.item is a dict
    def get_item_by_id(self, item_id):
        self.item = requests.get('{}/{}'.format(self.form_request_string(), item_id), headers=self.api_headers).json()
        return self.item

    # Works only with first level keys
    def patch_item_field(self, item_id, field_name, field_value):
        patch_url = ('{}/{}/'.format(self.form_request_string(), item_id))
        patch_string = {field_name: field_value}
        json_result_string = json.dumps(patch_string, ensure_ascii=False)
        print(patch_url + '    ' + json_result_string)
        requests.patch(patch_url, data=json_result_string.encode('utf-8'),
                       headers=self.api_headers)

    # Works only with second level keys
    def patch_item_subfield(self, item_id, field_name, subfield_name, field_value):
        patch_url = ('{}/{}/'.format(self.form_request_string(), item_id))
        patch_string = {field_name: {subfield_name: field_value}}
        json_result_string = json.dumps(patch_string, ensure_ascii=False)
        print(patch_url + '    ' + json_result_string)
        requests.patch(patch_url, data=json_result_string.encode('utf-8'),
                       headers=self.api_headers)

    # Works only with first level keys
    def get_item_id_by_the_field(self, field_name, field_value):
        for item in self.items_list:
            if item[field_name] == field_value:
                return item['id']
        return 'Item with {} equals {} does not exists'.format(field_name, field_value)
