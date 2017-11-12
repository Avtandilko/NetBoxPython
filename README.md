Example:

```python
BASE_API_URL = 'http://site.com/api/'
API_HEADERS = {
        'Authorization': 'Token *****',
        'Accept': 'application/json',
        'Content-Type': 'application/json'}
    
ITEM_GROUP = 'dcim'
ITEM_TYPE = 'devices'


if __name__ == "__main__":
    netbox = NetBoxPython(BASE_API_URL, API_HEADERS, ITEM_GROUP, ITEM_TYPE)
    netbox.form_request_string()
    netbox.get_all_items()
```
