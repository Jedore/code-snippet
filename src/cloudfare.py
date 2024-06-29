"""
@Author: jedor(https://github.com/jedore)
@Date: 29/06/2024
@brief: cloudfare
"""

import time

import requests

# https://developers.cloudflare.com/
# https://developers.cloudflare.com/api

headers = {
    'Authorization': 'Bearer <TOKEN>',
    'Content-Type': 'application/json',
}

# base_url = 'https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project_name}/deployments'
base_url = 'https://api.cloudflare.com/client/v4/accounts/55d951751494a1465d134083f39c7e4b/pages/projects/jedore/deployments'


def get_deployments(limit: int = 20):
    # Cloudfare limit one page count
    # https://developers.cloudflare.com/api/operations/pages-deployment-get-deployments
    params = {
        'page': 1,
        'per_page': limit,
        'sort_by': 'created_on',
        'sort_order': 'desc',
    }
    rsp = requests.get(base_url, headers=headers, params=params)
    if rsp.status_code != 200:
        raise Exception("Get deployments failed:", rsp.status_code, rsp.text)

    data = rsp.json()
    deployments = data['result']
    print("Get deployments:", len(deployments))
    return deployments


def del_deployments(deployments: list, retain: int = 5):
    # Retain the <retain> latest deployments
    # https://developers.cloudflare.com/api/operations/pages-deployment-delete-deployment
    for index, deployment in enumerate(deployments):
        if index < retain:
            continue

        uid = deployment["id"]
        url = base_url + f'/{uid}'
        try:
            rsp = requests.delete(url, headers=headers)
            if rsp.status_code != 200:
                print("Delete deployment failed:", index, uid, rsp.status_code, rsp.text)
            else:
                print("Delete:", index, uid)
        except Exception as e:
            print("Delete deployment failed:", index, uid, e)

        time.sleep(1)


if __name__ == '__main__':
    deployments = get_deployments()
    del_deployments(deployments, retain=3)
