# Enterprise Deployment & Operations Manual

## 1. System Requirements & Hardware Sizing

| Sizing Tier | Concurrency (Docs/Min) | CPU Cores | RAM | Storage |
| :--- | :--- | :--- | :--- | :--- |
| **Small / Development** | 100 - 500 | 4 Cores | 8 GB | 50 GB SSD |
| **Medium / Production** | 500 - 2,500 | 8 Cores | 16 GB | 200 GB NVMe |
| **Enterprise High Load** | 2,500 - 10,000+ | 16 Cores | 32 GB | 1 TB NVMe RAID |

---

## 2. Environment Variables Configuration

Create a production `.env` file in the project root:

```env
APP_NAME=Nexus DocIntel Enterprise
APP_ENV=production
DEBUG=false
SECRET_KEY=generate-a-cryptographically-secure-random-string-64-chars
ACCESS_TOKEN_EXPIRE_MINUTES=480
DATABASE_URL=sqlite:///./data/database/doc_intel.db
MAX_UPLOAD_SIZE_MB=50
WORKER_CONCURRENCY=4
HOST=0.0.0.0
PORT=8000
```

---

## 3. Production Service Configuration (Systemd / Service Manager)

```ini
[Unit]
Description=Nexus DocIntel Enterprise Document Processing Platform
After=network.target

[Service]
User=docintel
Group=docintel
WorkingDirectory=/opt/docintel/project-12
ExecStart=/opt/docintel/venv/bin/python run.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

---

## 4. Reverse Proxy Configuration (Nginx)

```nginx
server {
    listen 80;
    server_name docintel.enterprise.internal;
    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
