from imports import *
import time

api_key = "aliWCBJ6KZJ7RQ9UKJJ2KmTJFvClJWN43RHmbWho"
headers = {"Authorization": f"{api_key}", "Content-Type": "application/json"}


def run_query(query_id):
# Run query 
    # Set the API key and endpoint URL
    endpoint_url = f"https://redash-vn.ninjavan.co/api/queries/{query_id}/results"

    # Set the headers and data for the API request
    data = {
            "max_age": 0
            }

    # Make the POST request to the endpoint
    response = requests.post(endpoint_url, headers=headers,
                            json=data
                            )
    # get job status
    print("Job status: {}".format(response.json()['job']['status']))

    job_id = response.json()["job"]["id"]
    query_result_id = 0
    job_status = 1
    while job_status in [1, 2]:

        job_res = requests.get('https://redash-vn.ninjavan.co/api/jobs/{}?api_key={}'.format(job_id, api_key))
        job_status = job_res.json()['job']['status'] 
        if job_status == 4:
            print("Job failed: {}".format(job_res.json()['job']['error']))
            query_result_id =  0
        elif job_status == 3:
            print("Job success: {}".format(job_res.json()))
            query_result_id = job_res.json()['job']['query_result_id']
        else:
            print("Job running: {}".format(job_res.json()))
            
            time.sleep(5)

    # Get query result
    res = requests.get(endpoint_url, headers=headers,
                            json=data
                            )
    return res



