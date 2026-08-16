import os
import sys
import time
import requests
import kagglesdk
from kagglesdk.competitions.types.competition_api_service import (
    ApiStartSubmissionUploadRequest,
    ApiGetSubmissionLimitsRequest,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBMISSION_PATH = os.path.join(BASE_DIR, "submission.tar.gz")
COMPETITION_NAME = "pokemon-tcg-ai-battle"

print("=========================================================")
print("KAGGLE SUBMISSION UPLOADER — PTCG AI BATTLE CHALLENGE")
print("=========================================================")

client = kagglesdk.KaggleClient()

# Check submission limits
try:
    lim_req = ApiGetSubmissionLimitsRequest()
    lim_req.competition_name = COMPETITION_NAME
    limits = client.competitions.competition_api_client.get_submission_limits(lim_req)
    print(f"Submission Limits: {limits}")
except Exception as e:
    print(f"Note on limits: {e}")

# Prepare upload request
file_size = os.path.getsize(SUBMISSION_PATH)
mtime = int(os.path.getmtime(SUBMISSION_PATH))

upload_req = ApiStartSubmissionUploadRequest()
upload_req.competition_name = COMPETITION_NAME
upload_req.content_length = file_size
upload_req.file_name = "submission.tar.gz"
upload_req.last_modified_epoch_seconds = mtime

print(f"Requesting upload slot for: {SUBMISSION_PATH} ({file_size} bytes)...")
upload_res = client.competitions.competition_api_client.start_submission_upload(upload_req)
print(f"Upload Response: {upload_res}")

token = getattr(upload_res, "token", None) or getattr(upload_res, "token_string", None)
upload_url = getattr(upload_res, "create_url", None) or getattr(upload_res, "url", None)

print(f"Token: {token}")
print(f"Upload URL: {upload_url}")

if upload_url:
    print("Uploading submission.tar.gz bytes to Kaggle storage...")
    with open(SUBMISSION_PATH, "rb") as f:
        headers = {"Content-Type": "application/gzip", "Content-Length": str(file_size)}
        put_res = requests.put(upload_url, data=f, headers=headers)
        print(f"Upload HTTP Status: {put_res.status_code}")
        if put_res.status_code not in (200, 201):
            print(f"Upload Response Body: {put_res.text}")

print(f"SUCCESS: Uploaded {file_size} bytes. Token: {token}")
