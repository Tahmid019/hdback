# Changelog

## Role-Based Authorization (June 2026)

Added a hardcoded role-based permission system to the backend. No login/password required — designed to be replaced with JWT/session auth later.

### How It Works

1. One variable controls everything — `HARDCODED_ROLE` in `hd_backend/permissions.py` acts as the "currently logged-in" user. Change it to `"doctor"`, `"technician"`, or `"patient"` to simulate different users.

2. Each view declares who can access it — Views set a `required_roles` attribute (e.g. `required_roles = ['doctor', 'technician']`). If the attribute is missing, the endpoint is public (anyone can access).

3. Permission check on every request — `RoleBasedPermission` (applied globally via `settings.py`) checks if `HARDCODED_ROLE` is in the view's `required_roles`. If not → 403 Forbidden.

### Roles

| Role         | User              | Can Access                  |
|--------------|-------------------|-----------------------------|
| technician   | Tech. Maya Singh  | Dashboard + IoT ingestion   |
| doctor       | Dr. Aris Thorne   | Dashboard only              |
| patient      | James O'Brien     | Public endpoints only       |

### API Endpoints & Access

| Endpoint               | Method | Allowed Roles          | Description                          |
|------------------------|--------|------------------------|--------------------------------------|
| /api/auth/me/          | GET    | Public                 | Returns current user info            |
| /api/snapshot/         | GET    | Doctor, Technician     | Full machine state snapshot          |
| /api/section/\<name\>/ | GET    | Doctor, Technician     | Single section (ecg, pump, vitals)   |
| /api/wave/             | GET    | Doctor, Technician     | Waveform chunk for streaming         |
| /iot/ingest/           | POST   | Technician only        | Ingest a single section update       |
| /iot/ingest/bulk/      | POST   | Technician only        | Ingest multiple sections at once     |
| /iot/health/           | GET    | Public                 | Health check                         |
| ws://localhost:8000/ws/monitor/ | WS | -               | Real-time machine state updates      |

### Testing Authorization

```bash
# 1. Set the role in hd_backend/permissions.py
HARDCODED_ROLE = "patient"

# 2. Restart the container
docker compose restart web

# 3. Hit a protected endpoint — expect 403
curl http://localhost:8000/api/snapshot/
# Response: {"detail": "Your role does not have permission to access this resource."}

# 4. Change to "technician", restart — expect 200
curl http://localhost:8000/api/snapshot/
# Response: { ...full machine state JSON... }
```

### Files Changed

| File                        | Status   | What Changed                                               |
|-----------------------------|----------|------------------------------------------------------------|
| hd_backend/permissions.py   | 🆕 New   | HARDCODED_ROLE, role-user map, RoleBasedPermission class   |
| hd_backend/auth_views.py    | 🆕 New   | GET /api/auth/me/ — returns current user info              |
| hd_backend/settings.py      | ✏️ Modified | Added RoleBasedPermission as the default permission class  |
| hd_backend/urls.py          | ✏️ Modified | Added /api/auth/me/ route                                  |
| monitor/views.py            | ✏️ Modified | Added required_roles = ['doctor', 'technician'] to views   |
| iot/views.py                | ✏️ Modified | Added required_roles = ['technician'] to ingest views      |

> **Future:** Replace `HARDCODED_ROLE` with real JWT/session authentication. The `RoleBasedPermission` class just needs to read the role from `request.user` instead of the hardcoded variable.
