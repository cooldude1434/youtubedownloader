sequenceDiagram
    autonumber
    participant User as Bank Employee (React)
    participant IAP as Google Cloud IAP
    participant Azure as Azure AD (Entra ID)
    participant API as FastAPI (GKE)
    participant GCS as Cloud Storage

    Note over User, IAP: Phase 1: Authentication (SSO)
    User->>IAP: Access App URL
    IAP-->>User: Redirect to Azure AD Login
    User->>Azure: Provide Bank Credentials
    Azure-->>IAP: OIDC Token (Identity)
    IAP->>User: Set Session Cookie

    Note over User, GCS: Phase 2: Secure Upload (Proxy)
    User->>API: POST /upload (File + IAP JWT)
    API->>API: Validate IAP JWT Signature
    API->>API: Sanitize Filename & Check Mime-Type
    API->>GCS: Stream Upload (Service Account)
    GCS-->>API: 201 Created (raw/uuid.xlsx)
    API-->>User: 202 Accepted (Job ID: 123)

    Note over API, GCS: Phase 3: Async Processing
    rect rgb(240, 240, 240)
        API->>GCS: Read raw/uuid.xlsx
        API->>API: Run Reconciliation Logic
        API->>GCS: Write processed/uuid_result.xlsx
    end

    Note over User, GCS: Phase 4: Secure Download
    User->>API: GET /download/123
    API->>GCS: Generate Signed URL (GET)
    GCS-->>API: Signed URL (Expires in 10m)
    API-->>User: Redirect to Signed URL
    User->>GCS: Download File Directly
