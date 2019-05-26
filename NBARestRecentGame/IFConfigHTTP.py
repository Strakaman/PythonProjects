import requests
response = requests.get('http://ifconfig.co/json')
print(response.content)
print(response.content.decode('UTF-8'))
print(response.status_code)
print(response.ok)
