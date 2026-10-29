# API Integration Guide

## Status

This document proposes an API design. The recorded tests have not established a complete, implemented HTTP API contract. Treat the routes and payloads below as illustrative until implemented and tested.

## Design goals

- Version the API.
- Authenticate clients.
- Authorize every protected resource.
- Validate requests server-side.
- Use idempotency keys for operations that change state.
- Calculate authoritative accounting values on the trusted side.
- Return predictable error responses.
- Apply rate and request-size limits.
- Avoid leaking credentials or sensitive records.

## Proposed endpoints

| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| `GET` | `/health` | Basic service health |
| `POST` | `/v1/participants` | Register a participant |
| `GET` | `/v1/participants/{id}` | Retrieve authorized participant data |
| `POST` | `/v1/resources/contributions` | Submit a contribution request |
| `GET` | `/v1/resources/contributions/{id}` | Retrieve contribution status |
| `POST` | `/v1/transactions/validate` | Validate without committing |
| `GET` | `/v1/transactions/{id}` | Retrieve an authorized transaction |
| `POST` | `/v1/blocks/process` | Request block processing |
| `GET` | `/v1/blocks/{id}` | Retrieve a block |
| `GET` | `/v1/wallets/{id}/accounting` | Retrieve authorized accounting information |

These endpoints do not necessarily exist in the current application.

## Example request

```http
POST /v1/resources/contributions
Authorization: Bearer <access-token>
Content-Type: application/json
Idempotency-Key: <unique-request-id>

{
  "resource_type": "storage",
  "quantity": 1048576,
  "unit": "byte"
}
```

The server should authenticate and authorize the caller, validate the declaration, verify the contribution, calculate PPM, and persist the result. Do not trust a client-supplied PPM value as authoritative.

## Suggested response

```json
{
  "contribution_id": "server-generated-id",
  "status": "pending_verification"
}
```

This is an example, not a current API guarantee.

## Suggested status codes

- `200 OK`: successful read or completed operation.
- `201 Created`: resource created.
- `202 Accepted`: request accepted for asynchronous processing.
- `400 Bad Request`: malformed request.
- `401 Unauthorized`: authentication missing or invalid.
- `403 Forbidden`: caller lacks permission.
- `404 Not Found`: resource not found or intentionally concealed.
- `409 Conflict`: duplicate or conflicting operation.
- `413 Payload Too Large`: request exceeds limits.
- `422 Unprocessable Content`: valid syntax but invalid domain data.
- `429 Too Many Requests`: rate limit exceeded.
- `500 Internal Server Error`: unexpected server failure.
- `503 Service Unavailable`: required service unavailable.

Choose and document a consistent error schema before clients depend on it.

## Python client example

This example requires the proposed endpoint and authentication contract to be implemented first.

```python
import os
import uuid
import requests

base_url = os.environ["CROWD_CLOUD_API_URL"].rstrip("/")
token = os.environ["CROWD_CLOUD_API_TOKEN"]

response = requests.post(
    f"{base_url}/v1/resources/contributions",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Idempotency-Key": str(uuid.uuid4()),
    },
    json={
        "resource_type": "storage",
        "quantity": 1048576,
        "unit": "byte",
    },
    timeout=(3.05, 15),
)

response.raise_for_status()
print(response.json())
```

Install the HTTP client in a managed environment if required:
```bash
python -m pip install requests
```

Use HTTPS outside local development. Keep tokens out of source code and logs.

## Implementation recommendations

- Use a framework such as FastAPI if an HTTP API is selected.
- Define request and response schemas.
- Separate route handlers from domain logic.
- Authenticate and authorize all protected operations.
- Apply numeric bounds and finite-number validation.
- Make writes transactional.
- Implement idempotency and duplicate detection.
- Use pagination for collection endpoints.
- Define timeouts and bounded retries for external integrations.
- Add contract, integration, and security tests before public deployment.

## External integrations

For each provider integration, document credential scope, exchanged data, timeout behavior, retries, idempotency, rate limits, retention, failure behavior, and audit requirements.

Retries must not duplicate contributions or accounting updates.
