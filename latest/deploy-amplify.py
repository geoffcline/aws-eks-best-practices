import os
import boto3
from zipfile import ZipFile
import requests

def upload_file_to_url(file_path, url):
    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f)}
        response = requests.put(url, data=f)
        return response


def zip_directory(folder_path, zip_path):
    with ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, folder_path))


def create_deployment(app_id, branch_id):
    a_client = boto3.client('amplify')
    response = a_client.create_deployment(
        appId=app_id,
        branchName=branch_id
    )
    return response


def start_deployment(app_id, branch_id, job_id):
    a_client = boto3.client('amplify')
    response = a_client.start_deployment(
        appId=app_id,
        branchName=branch_id,
        jobId=job_id
    )
    return response

# need to set env var for AWS_PROFILE before running
# aws amplify create-app --name MyDocs2 --enable-basic-auth --basic-auth-credentials $(echo -n "aws:preview" | base64)
# aws amplify create-branch --app-id=d1uiikpnb46qaz --branch-name dev2

def driver():
    directory_to_zip = '/home/gcline/workplace/bpg-eks/src/AmazonEKSBestPracticesDocs/build/server-root/EKS/latest/userguide'
    zip_file_name = 'artifacts.zip'
    app_id = 'd1uiikpnb46qaz'
    branch_id = 'bpg-adoc'

    zip_directory(directory_to_zip, zip_file_name)

    r = create_deployment(app_id, branch_id)

    upload_url = r['zipUploadUrl']
    job_id = r['jobId']
    print('created job: ' + job_id)

    upload_file_to_url(zip_file_name, upload_url)

    r = start_deployment(app_id, branch_id, job_id)
    print('started deployment: ' + job_id)
    return


if __name__ == "__main__":
    driver()



