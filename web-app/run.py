import requests

def get_jenkins_crumb(jenkins_url, username, api_token):
    response = requests.get(f'{jenkins_url}/crumbIssuer/api/json', auth=(username, api_token))
    response.raise_for_status()  # Raise an error for bad status codes
    crumb_data = response.json()
    crumb_value = crumb_data['crumb']
    crumb_field = crumb_data['crumbRequestField']
    return crumb_field, crumb_value

jenkins_url = 'http://localhost:8080'
username = 'admin'
api_token = '1178a500952508d5a2ed404e2a6457905b'

crumb_field, crumb_value = get_jenkins_crumb(jenkins_url, username, api_token)
print(f"Crumb Field: {crumb_field}, Crumb Value: {crumb_value}")

