"""
@Author: Jedore(https://github.com/jedore)
@Date: 29/06/2024
@brief: vercel
"""

import time

import requests

# https://vercel.com/docs/rest-api

headers = {
    'Authorization': 'Bearer <TOKEN>',
    'Content-Type': 'application/json',
}

base_url = 'https://api.vercel.com'


def get_deployments(project_id: str = '', limit: int = 100):
    # https://vercel.com/docs/rest-api/endpoints/deployments#list-deployments

    url = base_url + '/v6/deployments'
    params = {
        'limit': limit,
        'projectId': project_id,
    }
    rsp = requests.get(url, headers=headers, params=params)
    if rsp.status_code != 200:
        raise Exception("Get deployments failed:", rsp.status_code, rsp.text)

    data = rsp.json()
    deployments = data['deployments']
    if len(deployments) == limit:
        time.sleep(2)
        # get all deployments once
        return get_deployments(project_id=project_id, limit=limit + 50)

    sorted_deployments = sorted(deployments, key=lambda k: k['created'], reverse=True)
    print("Get deployments:", len(sorted_deployments))
    return sorted_deployments


def del_deployments(deployments: list, retain: int = 5):
    # Retain the <retain> latest deployments
    # https://vercel.com/docs/rest-api/endpoints/deployments#delete-a-deployment
    for index, deployment in enumerate(deployments):
        if index < retain and deployment["state"] == "READY":
            continue

        uid = deployment["uid"]
        url = base_url + f'/v13/deployments/{uid}'
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
    project_ids = []
    for project_id in project_ids:
        deployments = get_deployments(project_id=project_id)
        del_deployments(deployments)
