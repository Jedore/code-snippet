"""
@Author: jedor(https://github.com/jedore)
@Date: 29/06/2024
@brief: github
"""
import time

import requests

headers = {
    'Authorization': 'Bearer <TOKEN>',
    'Accept': 'application/vnd.github+json',
    'Content-Type': 'application/json',
}

# base_url = 'https://api.github.com/repos/OWNER/REPO/deployments'
base_url = 'https://api.github.com/repos/Jedore/Jedore.github.io/deployments'
# base_wk_url = "https://api.github.com/repos/OWNER/REPO/actions/runs"
base_wk_url = "https://api.github.com/repos/Jedore/Jedore.github.io/actions/runs"


def get_deployments(env: str = '', limit: int = 100):
    # https://docs.github.com/en/rest/deployments/deployments?apiVersion=2022-11-28#list-deployments

    params = {
        'page': 1,
        'per_page': limit,
        'environment': env,
    }
    rsp = requests.get(base_url, headers=headers, params=params)
    if rsp.status_code != 200:
        raise Exception("Get deployments failed:", rsp.status_code, rsp.text)

    data = rsp.json()
    print("Get deployments:", len(data))
    return data


def del_deployments(deployments: list, retain: int = 5):
    # Retain the <retain> latest deployments
    # https://docs.github.com/en/rest/deployments/deployments?apiVersion=2022-11-28#delete-a-deployment
    for index, deployment in enumerate(deployments):
        if index < retain:
            continue

        uid = deployment["id"]
        url = base_url + f'/{uid}'
        try:
            rsp = requests.delete(url, headers=headers)
            if rsp.status_code != 204:
                print("Delete deployment failed:", index, uid, rsp.status_code, rsp.text)
            else:
                print("Delete:", index, uid)
        except Exception as e:
            print("Delete deployment failed:", index, uid, e)

        time.sleep(0.5)

def get_workflow_runs(env: str = '', limit: int = 100):
    # https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28#list-workflow-runs-for-a-repository

    params = {
        'page': 1,
        'per_page': limit,
        # 'environment': env,
    }
    rsp = requests.get(base_wk_url, headers=headers, params=params)
    if rsp.status_code != 200:
        raise Exception("Get workflow runs failed:", rsp.status_code, rsp.text)

    data = rsp.json()
    runs = data['workflow_runs']
    print("Get workflow runs:", len(runs))
    return runs


def del_workflow_runs(runs: list, retain: int = 5):
    # Retain the <retain> latest deployments
    # https://vercel.com/docs/rest-api/endpoints/deployments#delete-a-deployment
    for index, run in enumerate(runs):
        if index < retain:
            continue

        uid = run["id"]
        url = base_wk_url + f'/{uid}'
        try:
            rsp = requests.delete(url, headers=headers)
            if rsp.status_code != 204:
                print("Delete workflow run failed:", index, uid, rsp.status_code, rsp.text)
            else:
                print("Delete workflow run:", index, uid)
        except Exception as e:
            print("Delete workflow run failed:", index, uid, e)

        time.sleep(1)



if __name__ == '__main__':
    while True:
        runs = get_workflow_runs()
        del_workflow_runs(runs, 0)

        deployments = get_deployments(env='github-pages')
        del_deployments(deployments, retain=50)

        deployments = get_deployments(env='Production')
        del_deployments(deployments, retain=0)
