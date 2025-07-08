# Facet Backdoor API

## Wasabi and AWS STS Compatibility

**Wasabi does not support the AWS STS `get_session_token` API.**

- You cannot generate temporary credentials with Wasabi like you can with AWS.
- You must use your static Wasabi access/secret keys, or manage IAM via the Wasabi console.

### What to do:

- Remove or disable the `/token/aws` endpoint if you are only using Wasabi.
- Clearly document in your API and UI that temporary credentials are not available with Wasabi.
- If you want to support both AWS and Wasabi, you can check the endpoint or a config flag and raise a clear error if the user tries to use `/token/aws` with Wasabi.

#### Options:

- Remove the `/token/aws` endpoint,
- Replace it with a clear error message,
- Or add logic to detect Wasabi and return a helpful response.
