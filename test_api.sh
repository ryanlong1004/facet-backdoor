#!/bin/bash
# Warn if using placeholder credentials
if [[ "$AWS_ACCESS_KEY_ID" == "YOUR_ACCESS_KEY" || "$AWS_SECRET_ACCESS_KEY" == "YOUR_SECRET_KEY" || "$AWS_SESSION_TOKEN" == "YOUR_SESSION_TOKEN" ]]; then
  echo "[ERROR] You must set valid AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_SESSION_TOKEN before running this test."
  exit 2
fi
# test_api.sh - Test FastAPI S3 presigned GET URL endpoint


API_URL="http://127.0.0.1:9650"
# Set your S3/Wasabi credentials here or export them as env vars before running


# Load credentials from .env if present
if [ -f .env ]; then
  export $(grep -v '^#' .env | grep -E 'VITE_ACCESS_KEY|VITE_SECRET_KEY|VITE_BUCKET_REGION|VITE_BUCKET_ENDPOINT|VITE_BUCKET_NAME' | xargs)
fi

AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-${VITE_ACCESS_KEY}}"
AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-${VITE_SECRET_KEY}}"
# Session token is not in .env; user must provide if needed
AWS_SESSION_TOKEN="${AWS_SESSION_TOKEN:-YOUR_SESSION_TOKEN}"
REGION="${REGION:-${VITE_BUCKET_REGION:-us-east-1}}"
ENDPOINT="${ENDPOINT:-${VITE_BUCKET_ENDPOINT:-https://s3.us-east-1.wasabisys.com}}"
BUCKET="${BUCKET:-${VITE_BUCKET_NAME:-pavlo-ui-demo}}"
KEY="${KEY:-/jobs/2025_07_08/324ac7ad-7651-4fb5-927f-34a0fa13ccc7/faces/thumbnails/cb62bbd920e5db0280e050fe8a7d0be4662aaf3ebc612e5dc0313026e1dc22ab.jpg}"
EXPIRATION=3600



echo "Testing presigned GET URL endpoint with S3/Wasabi credentials..."

# 2. Request presigned PUT URL
echo "Requesting presigned PUT URL..."
PUT_URL=$(curl -s -X POST "$API_URL/presigned/put" \
  -H "x-aws-access-key-id: $AWS_ACCESS_KEY_ID" \
  -H "x-aws-secret-access-key: $AWS_SECRET_ACCESS_KEY" \
  -H "x-aws-session-token: $AWS_SESSION_TOKEN" \
  -H "X-Region: $REGION" \
  -H "X-Endpoint: $ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{"bucket":"'$BUCKET'","key":"'$KEY'","expiration":'$EXPIRATION'}' | jq -r .url)

if [ "$PUT_URL" == "null" ] || [ -z "$PUT_URL" ]; then
  echo "Failed to get presigned PUT URL."
  exit 1
fi

echo "Presigned PUT URL: $PUT_URL"

# 3. Use the presigned PUT URL to upload a test file
echo "Testing presigned PUT URL (uploading this script as test file)..."
curl -v -X PUT -T "$0" "$PUT_URL"


# 4. Request presigned GET URL
echo "Requesting presigned GET URL..."
URL=$(curl -s -X POST "$API_URL/presigned/get" \
  -H "x-aws-access-key-id: $AWS_ACCESS_KEY_ID" \
  -H "x-aws-secret-access-key: $AWS_SECRET_ACCESS_KEY" \
  -H "x-aws-session-token: $AWS_SESSION_TOKEN" \
  -H "X-Region: $REGION" \
  -H "X-Endpoint: $ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{"bucket":"'$BUCKET'","key":"'$KEY'","expiration":'$EXPIRATION'}' | jq -r .url)

if [ "$URL" == "null" ] || [ -z "$URL" ]; then
  echo "Failed to get presigned URL."
  exit 1
fi

echo "Presigned URL: $URL"

# 3. Use the presigned URL to GET the object
echo "Testing presigned URL..."
curl -v "$URL"
