# Timely

Timely is a local-only (LAN) attendance product with a FastAPI backend, Next.js admin portal, and Flutter mobile app.

## Repository Layout

- `backend/` FastAPI API + SQLAlchemy models + pytest tests
- `web/` Next.js admin UI
- `mobile/` Flutter mobile app
- `deploy/` Docker compose + Nginx reverse proxy

## Setup

### Requirements

- Docker + Docker Compose

### Start the stack

```bash
docker compose -f deploy/docker-compose.yml up --build
```

The admin portal will be available at `http://<server-ip>/` and the API at `http://<server-ip>/api`.

### Create the first Super Admin

1. Start the stack.
2. Connect to the API container and run the seed script:

```bash
docker compose -f deploy/docker-compose.yml exec api python -m app.seed
```

### LAN-only usage

- Pair the mobile app using the server IP configured in setup.
- Clock in/out works only when the server is reachable via IP and a valid nonce challenge is signed by the device.

## API

FastAPI serves OpenAPI docs at `/docs`.

## Testing

```bash
cd backend
pytest
```

## Troubleshooting

- **LAN access**: ensure the mini PC has a static IP and firewall allows ports 80/8000/3000.
- **Mobile pairing**: confirm the base URL is the server IP (no DNS required).
- **SMTP**: configure in setup; if SMTP is unavailable, admins can download reports from the Reports page.

## Notes

- D17 leave-building detection is intentionally not implemented in v1.0.
- Site tracking/proxy/DNS logging is intentionally omitted.
