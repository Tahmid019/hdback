# Changelog

## Feature: Role-Based Access Control (RBAC) & JWT Authentication (July 2026)

This release overhauls the authentication and authorization system. We have completely removed the temporary hardcoded role mechanism and replaced it with a robust, stateless JSON Web Token (JWT) authentication layer, paired with view-level role-based permissions.

### Key Enhancements

1. **JWT Authentication Layer (`rest_framework_simplejwt`)**
   - Implemented JWT-based login using email and password.
   - Introduced `CustomJWTAuthentication` (in `hd_backend/authentication.py`). Instead of querying the database on every single API request to retrieve the user's role, the JWT payload itself contains the user's `role` claim. The authentication class decodes the token and constructs a stateless `User` object in memory which is then populated using the JWT. This eliminates database overhead for authenticated requests.

2. **Role-Based Permission Enforcement**
   - Introduced `RoleBasedPermission` (in `hd_backend/permissions.py`) as the default global permission class for all DRF views.
   - **How it works:** Views can now define a `required_roles` list (e.g., `required_roles = ['doctor', 'technician']`). The permission class inspects `request.user.role` (which was attached by the JWT middleware) and ensures it intersects with the view's requirements.
   - **Default Behavior:** If a view omits the `required_roles` attribute, it defaults to being a **public endpoint** (no auth required).
   - If authorization fails, the system returns a `403 Forbidden` with a standardized error message.

3. **User Management (`accounts` App)**
   - The custom `User` model (`accounts.User`) natively supports the `role` field.
   - Created a new Django management command `seed_users` to facilitate local development and automated testing.

### 👥 Roles & Access Matrix

We support three distinct roles, mapping to the following business logic rules:

| Role         | Description | Test User Account       | Password  | Core Capabilities |
|--------------|-------------|-------------------------|-----------|-------------------|
| **Technician** | Equipment operator | `tech@test.com`         | `test1234`| Full access. Can view the Dashboard, request Waveform streams, and push (POST) IoT sensor data telemetry. |
| **Doctor**     | Medical supervisor | `doctor@test.com`       | `test1234`| Read-only access. Can view the Dashboard and Machine Snapshot data, but cannot ingest IoT data or stream high-freq waveforms. |
| **Patient**    | End user | `patient@test.com`      | `test1234`| Extremely limited. Can only access public health checks and unauthenticated fallback views. |

### 🛣️ API Endpoints Summary

#### Authentication Endpoints (New)
- `POST /api/auth/login/` - Takes `email` and `password`, returns `access` and `refresh` tokens.
- `POST /api/auth/refresh/` - Takes a `refresh` token, issues a new `access` token.
- `GET /api/auth/me/` - Returns the currently authenticated user's ID, name, and role.

#### Monitor & Dashboard Endpoints
- `GET /api/snapshot/` - Requires: `['doctor', 'technician']`
- `GET /api/section/<name>/` - Requires: `['doctor', 'technician']`
- `GET /api/wave/` - Requires: `['technician']`

#### IoT Ingestion Endpoints
- `POST /iot/ingest/` - Requires: `['technician']`
- `POST /iot/ingest/bulk/` - Requires: `['technician']`

#### System Health
- `GET /iot/health/` - Public endpoint

### 🛠️ Developer Workflow & Testing

To test the RBAC implementation locally, follow this flow:

1. **Seed the Test Users**
   Populate the database with the predefined test accounts (creates the Doctor, Technician, and Patient users).
   ```bash
   python manage.py seed_users
   ```

2. **Run the Automated Batch Tests**
   The integration test script has been heavily expanded to verify JWT token generation, role parsing, and access denial.
   ```bash
   test_backend.bat
   ```
   *Note: Tests 26 through 34 specifically validate the new JWT flow, verifying that Doctors are denied from Wave endpoints, Patients are denied from Pump endpoints, etc.*

### 📄 Detailed File Changes

- **`hd_backend/settings.py`**: Added `rest_framework_simplejwt`, configured JWT token lifetimes (30m access, 7d refresh), and wired up `CustomJWTAuthentication` and `RoleBasedPermission` as defaults.
- **`hd_backend/authentication.py`**: 🆕 Created `CustomJWTAuthentication` subclassing `JWTAuthentication` for stateless user initialization.
- **`hd_backend/permissions.py`**: 🆕 Created `RoleBasedPermission` to dynamically check `view.required_roles`. Removed old hardcoded role strings.
- **`hd_backend/urls.py`**: ✏️ Registered `/api/auth/login/`, `/api/auth/refresh/`, and `/api/auth/me/`.
- **`hd_backend/auth_views.py`**: 🆕 Implemented `CurrentUserView` for the `/api/auth/me/` endpoint.
- **`accounts/management/commands/seed_users.py`**: 🆕 Created the data seeder command.
- **`monitor/views.py` & `iot/views.py`**: ✏️ Annotated all critical DRF views with the appropriate `required_roles` attribute.
- **`test_backend.bat`**: ✏️ Upgraded script to execute `curl` requests with JWT Bearer headers and handle positive/negative assertions.
