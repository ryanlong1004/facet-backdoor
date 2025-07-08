#!/bin/bash
# test_api.sh - Test FastAPI S3 presigned GET URL endpoint

API_URL="http://127.0.0.1:8000"
ENV_FILE="../env"

# Read credentials from env file
USERNAME="testuser"   # TODO: set your username
PASSWORD="testpass"   # TODO: set your password
BUCKET="pavlo-ui-demo"  # TODO: set your bucket
KEY="/jobs/2025_07_08/324ac7ad-7651-4fb5-927f-34a0fa13ccc7/faces/thumbnails/cb62bbd920e5db0280e050fe8a7d0be4662aaf3ebc612e5dc0313026e1dc22ab.jpg"      # TODO: set your object key
EXPIRATION=3600

# Extract client_id and client_secret from env file (for other uses if needed)
CLIENT_ID=$(grep -E '^VITE_AUTH0_CLIENT_ID=' "$ENV_FILE" | cut -d'=' -f2-)
CLIENT_SECRET=$(grep -E '^VITE_SECRET_KEY=' "$ENV_FILE" | cut -d'=' -f2-)

# 1. Get JWT token
echo "Getting JWT token..."
TOKEN=$(curl -s -X POST "$API_URL/token/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$USERNAME&password=$PASSWORD" | jq -r .access_token)

echo "Token: $TOKEN"

# 2. Get presigned GET URL
echo "Requesting presigned GET URL..."
RESPONSE=$(curl -s -X POST "$API_URL/presigned/get" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"bucket": "'$BUCKET'", "key": "'$KEY'", "expiration": '$EXPIRATION'}')

echo "Presigned GET URL response: $RESPONSE"
