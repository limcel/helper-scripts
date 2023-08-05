import requests
from time import perf_counter

# Values to Set
username = "" # set github username
repo = "" # set github repository
token = "" # set github token
workflow_id = "" # seete github workflow ID
start_page = 0 # set page to start deleting from
end_page = 5 # set page to stop deleting from

startTime = perf_counter()

def timer():
    return "{:>10.4f}".format(perf_counter() - startTime)

headers = {
	"Accept": "application/vnd.github+json",
	"Authorization": f"Bearer {token}",
	"Content-Type": "application/json"
}

for page_number in range(start_page, end_page):
    # actions docs: https://docs.github.com/en/rest/actions/workflow-runs?apiVersion=2022-11-28#list-workflow-runs-for-a-workflow
	url = f'https://api.github.com/repos/{username}/{repo}/actions/workflows/{workflow_id}/runs?per_page=100&page={page_number}'
	r = requests.get(url, headers=headers)
	all_workflow_runs = r.json().get("workflow_runs")

	for i in all_workflow_runs:
		workflow_run_id = i.get("id")
		workflow_name = i.get("name")
        print(f'deleting {workflow_run_id}, page {page_number}')
        workflow_url_to_delete = f'https://api.github.com/repos/{username}/{repo}/actions/runs/{workflow_run_id}'
        requests.delete(workflow_url_to_delete, headers=headers)

print(f'Finished deleting {end_page - start_page} pages of workflows in {timer()} seconds!')