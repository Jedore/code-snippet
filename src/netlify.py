"""
@Author: jedor(https://github.com/jedore)
@Date: 29/06/2024
@brief: netlify
"""
import time

import requests

# https://docs.netlify.com/api/get-started
# https://open-api.netlify.com/

headers = {
    'Authorization': 'Bearer <TOKEN>',
    'Content-Type': 'application/json',
}

base_url = 'https://api.netlify.com/api/v1'


def get_deployments(site_id: str = '', limit: int = 100):
    # https://api.netlify.com/api/v1/sites/{site_id}/deploys
    # return deployments by create time desc

    url = base_url + f'/sites/{site_id}/deploys'
    params = {'per_page': limit}
    rsp = requests.get(url, headers=headers, params=params)
    if rsp.status_code != 200:
        raise Exception("Get deployments failed:", rsp.status_code, rsp.text)

    deployments = rsp.json()
    if len(deployments) == limit:
        time.sleep(2)
        # get all deployments once
        return get_deployments(site_id=site_id, limit=limit + 50)

    print("Get deployments:", len(deployments))
    return deployments


def del_deployments(deployments: list, retain: int = 5):
    # Retain the <retain> latest deployments
    #
    for index, deployment in enumerate(deployments):
        if index < retain:
            continue

        uid = deployment["id"]
        url = base_url + f'/deploys/{uid}'
        try:
            rsp = requests.delete(url, headers=headers)
            if rsp.status_code != 204:
                print("Delete deployment failed:", index, uid, rsp.status_code, rsp.text)
            else:
                print("Delete:", index, uid)
        except Exception as e:
            print("Delete deployment failed:", index, uid, e)

        time.sleep(1)


if __name__ == '__main__':
    site_ids = []
    for site_id in site_ids:
        deployments = get_deployments(site_id=site_id)
        del_deployments(deployments, retain=3)
