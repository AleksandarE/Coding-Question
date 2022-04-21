import json
import requests
import argparse
from os import environ

GITHUB_USER_ENDPOINT = 'https://api.github.com/user'


def obtain_os_env_var(var_name):
    if var_name in environ:
        return environ[var_name]
    else:
        return None

def get_authenticated_github_user(url, token):
    try:
        response = requests.get(url, headers={'Authorization': 'token ' + token})
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(e)
        return None

def get_console_arguments():
    parser = argparse.ArgumentParser(description='GitHub to Freshdesk')
    parser.add_argument('--username', '-u', help='GitHub Username', metavar='USERNAME')
    parser.add_argument('--fdesk-sd', '-f', help='Freshdesk Subdomain', metavar='SD')
    args = parser.parse_args()
    github_user = args.username
    freshdesk_subdomain = args.fdesk_sd
    return (github_user, freshdesk_subdomain)


def create_freshdesk_user_info(github_user_info):
    return {
        'name': github_user_info['login'],
        'unique_external_id': github_user_info['id'],
        'email': github_user_info['email'] if github_user_info['email'] != 'null' else 'N/A',
        'twitter_id': github_user_info['twitter_username'] if github_user_info['twitter_username']  != 'null' else 'N/A'
    }


def check_if_freshdesk_user_exists(freshdesk_subdomain, freshdesk_token, freshdesk_user_info):
    url = 'https://' + freshdesk_subdomain + '.freshdesk.com/api/v2/contacts/autocomplete'
    params = {'name': freshdesk_user_info['name']}
    response = requests.get(url, params=params, auth=(freshdesk_token, 'X'))
    if response.status_code == 200:
        response_text = response.text
        users = json.loads(response_text)
        if len(users) == 0:
            return -2
        elif len(users) == 1:
            return users[0]['id']
        else:
            return -1
    else:
        return -3


def create_freshdesk_user(freshdesk_subdomain, freshdesk_token, freshdesk_user_info):
    url = 'https://' + freshdesk_subdomain + '.freshdesk.com/api/v2/users'
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = freshdesk_user_info
    response = requests.post(url, headers=headers, json=json_data, auth=(freshdesk_token, 'X'))
    if response.status_code == 201:
        print('User created successfully.')
    else:
        print('User creation failed.')


def update_freshdesk_user(freshdesk_subdomain, freshdesk_token, freshdesk_user_info, id):
    url = 'https://' + freshdesk_subdomain + '.freshdesk.com/api/v2/contacts/' + str(id)
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = freshdesk_user_info
    response = requests.put(url, headers=headers, json=json_data, auth=(freshdesk_token, 'X'))
    if response.status_code == 200:
        print('User updated successfully.')
    else:
        print('User update failed.')

def main():
    args = get_console_arguments()
    github_user = args[0]
    freshdesk_subdomain = args[1]

    github_token = obtain_os_env_var('GITHUB_TOKEN')
    freshdesk_token = obtain_os_env_var('FRESHDESK_TOKEN')

    if github_token is None:
        print('GitHub Token not found. Please set the GITHUB_TOKEN environment variable.')
        return
    try:
        github_user_info = get_authenticated_github_user(GITHUB_USER_ENDPOINT, github_token)
        if github_user_info is None:
            print('GitHub Information not found. Please check your token.')
            return
        
        github_user_name = github_user_info['login']
    except Exception as e:
        print(e)
        return

    if github_user != github_user_info['login']:
        print('GitHub User is not the owner of the configured token. Please check your token.')
        return
    freshdesk_user_info = create_freshdesk_user_info(github_user_info)
    id = check_if_freshdesk_user_exists(freshdesk_subdomain, freshdesk_token, freshdesk_user_info)
    if id == -1:
        print('More than one user found. Please narrow your search.')
    elif id == -3:
        print('Freshdesk API error. Please check your token or subdomain')
    elif id == -2:
        create_freshdesk_user(freshdesk_subdomain, freshdesk_token, freshdesk_user_info) 
    else:
        update_freshdesk_user(freshdesk_subdomain, freshdesk_token, freshdesk_user_info, id)


if __name__ == '__main__':
    main()