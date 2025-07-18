# 🔐 OAuth + AWS Pre-signed URL Workflow

A full-stack template for securely uploading and downloading files using OAuth authentication and AWS pre-signed URLs.

---

## ⚙️ Tech Stack

- **Frontend**: Vue 3 + Pinia  
- **Backend**: FastAPI (Python)  
- **Storage**: AWS S3 (or Wasabi-compatible S3)  
- **Auth Provider**: Auth0 or Google OAuth  

---

## 🎯 Features

✅ OAuth login via Auth0  
✅ Backend token verification  
✅ Secure pre-signed URL generation  
✅ Frontend upload/download using S3  

---

## 🧭 Workflow Overview

```mermaid
sequenceDiagram
  participant User
  participant Frontend
  participant AuthProvider (OAuth)
  participant Backend API
  participant AWS S3

  User->>Frontend: Access web app
  Frontend->>AuthProvider: Redirect to OAuth login
  AuthProvider-->>Frontend: OAuth Access Token (ID token)
  Frontend->>Backend API: Send ID token in Authorization header
  Backend API->>AuthProvider: Verify token / Get user info
  Backend API->>AWS S3: Generate pre-signed URL
  Backend API-->>Frontend: Return pre-signed URL
  Frontend->>AWS S3: Upload/download using pre-signed URL
```

---

## 🖥️ Frontend (Vue 3 + Pinia)

### 🔑 OAuth Login (Auth0)

```ts
// composables/useAuth.ts
import { useAuth0 } from '@auth0/auth0-vue'

export const useAuth = () => {
  const auth0 = useAuth0()

  const login = () => auth0.loginWithRedirect()
  const logout = () => auth0.logout()
  const token = computed(() => auth0.getAccessTokenSilently())

  return { login, logout, token }
}
```

### 📡 Requesting Pre-signed URLs

```ts
// services/api.ts
export async function getPresignedUrl(fileName: string, type: 'put' | 'get') {
  const token = await auth.getAccessTokenSilently()
  const res = await fetch(`/api/presign-url`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ fileName, type }),
  })
  return res.json()
}
```

---

## 🧠 Backend (FastAPI)

### 🔒 Token Validation

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.auth_public_key, algorithms=["RS256"])
        return payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")
```

### 🔗 Generate Pre-signed URLs

```python
from fastapi import APIRouter, Depends
import boto3

router = APIRouter()

@router.post("/presign-url")
def get_presigned_url(request: dict, user_id: str = Depends(get_current_user)):
    s3 = boto3.client('s3',
                      aws_access_key_id=settings.aws_access_key,
                      aws_secret_access_key=settings.aws_secret_key)

    if request['type'] == 'put':
        url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={'Bucket': settings.bucket, 'Key': request['fileName']},
            ExpiresIn=3600
        )
    elif request['type'] == 'get':
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': settings.bucket, 'Key': request['fileName']},
            ExpiresIn=3600
        )
    return {"url": url}
```

---

## 🔐 Auth Provider Setup

1. Set **Allowed Callback URLs** to your frontend domain  
2. Enable **RS256** token signing  
3. Set scopes: `openid profile email`  
4. Store public key in `.env` or `settings.py`

---

## 🚀 Optional Enhancements

| Feature                        | Benefit                                      |
|-------------------------------|----------------------------------------------|
| JWT Caching                   | Reduce token validation overhead             |
| Role-based access             | Control who can request `put` vs `get`       |
| Audit logging                 | Track uploads/downloads                      |
| Rate limiting                 | Prevent abuse of signed URLs                 |
| Expiring Tokens               | Set `ExpiresIn` for fine-grained access      |

---

## ✅ Summary

- 🔐 Frontend handles OAuth and gets JWT  
- 🧠 Backend validates JWT and signs S3 URLs  
- 🗂️ Pre-signed URLs protect your bucket from public access  
- 🧼 Clean, modular architecture using best practices  

---

## 📁 Project Structure

```
project-root/
│
├── frontend/                 # Vue 3 app
│   └── composables/useAuth.ts
│   └── services/api.ts
│
├── backend/                  # FastAPI app
│   └── main.py
│   └── routes/presign_url.py
│   └── auth/token_verifier.py
│
├── .env                      # Auth and AWS credentials
└── README.md                 # This file
```

---

## 📌 License

MIT © YourName
