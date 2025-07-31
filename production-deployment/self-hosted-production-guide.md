# Prefect Server Setup Documentation (Server-1)

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Python and Virtual Environment Setup](#python-and-virtual-environment-setup)
3. [Prefect Installation and Configuration](#prefect-installation-and-configuration)
4. [System Service Configuration](#system-service-configuration)
5. [Nginx Configuration](#nginx-configuration)
6. [Directory Structure and Permissions](#directory-structure-and-permissions)
7. [Common Issues and Solutions](#common-issues-and-solutions)
8. [Verification Steps](#verification-steps)

## Prerequisites

- Ubuntu/Debian-based system
- Python 3.12.3
- Nginx installed
- SSL certificates (using Certbot)
- Root or sudo access

## Python and Virtual Environment Setup

```bash
# Create virtual environment using uv
uv venv /opt/.venv --python 3.12

# Activate virtual environment
source /opt/.venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

## Prefect Installation and Configuration

### Install Prefect

```bash
# Install Prefect
uv pip install prefect==3.4.10
```

### Create Required Directories and User

```bash
# Create prefect user
sudo useradd -r -s /bin/false prefect

# Create necessary directories
sudo mkdir -p /etc/prefect
sudo mkdir -p /var/lib/prefect
sudo mkdir -p /var/log/prefect
sudo mkdir -p /home/prefect/.prefect

# Set proper ownership
sudo chown -R prefect:prefect /etc/prefect
sudo chown -R prefect:prefect /var/lib/prefect
sudo chown -R prefect:prefect /var/log/prefect
sudo chown -R prefect:prefect /home/prefect
sudo chown -R prefect:prefect /opt/.venv
```

### Configure Prefect Environment

Create `/etc/prefect/server.env`:

```bash
sudo tee /etc/prefect/server.env << 'EOF'
PREFECT_SERVER_API_HOST=127.0.0.1
PREFECT_SERVER_API_PORT=4200
PREFECT_SERVER_DATABASE_CONNECTION_URL=sqlite+aiosqlite:////var/lib/prefect/prefect.db
PREFECT_UI_API_URL=https://prefect.yourdomain.com/api
EOF
```

## System Service Configuration

Create systemd service file `/etc/systemd/system/prefect-server.service`:

```bash
sudo tee /etc/systemd/system/prefect-server.service << 'EOF'
[Unit]
Description=Prefect Server
After=network.target

[Service]
Type=simple
User=prefect
Group=prefect
EnvironmentFile=/etc/prefect/server.env
WorkingDirectory=/var/lib/prefect

# Ensure the service has access to necessary directories
ReadWritePaths=/var/lib/prefect
ReadWritePaths=/opt/.venv
ReadWritePaths=/home/prefect/.prefect

ExecStart=/opt/.venv/bin/prefect server start
Restart=always
RestartSec=5

# Set environment variables
Environment=HOME=/home/prefect
Environment=PYTHONPATH=/opt/.venv/lib/python3.12/site-packages

[Install]
WantedBy=multi-user.target
EOF
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable prefect-server
sudo systemctl start prefect-server
```

## Nginx Configuration

Create Nginx configuration file `/etc/nginx/sites-available/prefect.yourdomain.com`:

```nginx
server {
    server_name prefect.yourdomain.com;
    # Proxy headers
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    # WebSocket support
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_buffering off;
    # Increase timeouts for long-running requests
    proxy_read_timeout 300s;
    proxy_connect_timeout 75s;
    location / {
        proxy_pass http://127.0.0.1:4200;
        # Add CORS headers
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE' always;
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization' always;
        add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range' always;

        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE';
            add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }
    }
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/prefect.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/prefect.yourdomain.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}
server {
    if ($host = prefect.yourdomain.com) {
        return 301 https://$host$request_uri;
    }
    listen 80;
    server_name prefect.yourdomain.com;
    return 404;
}
```

Enable the configuration:

```bash
sudo ln -s /etc/nginx/sites-available/prefect.yourdomain.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Directory Structure and Permissions

Important directories and their permissions:

```bash
/opt/.venv                     # Virtual environment (prefect:prefect)
/etc/prefect                   # Configuration files (prefect:prefect)
/var/lib/prefect              # Prefect data directory (prefect:prefect)
/var/log/prefect              # Log files (prefect:prefect)
/home/prefect/.prefect        # Prefect user home directory (prefect:prefect)
```

## Common Issues and Solutions

### 1. Permission Denied Errors

**Issue:** PermissionError when accessing UI build directory

**Solution:**
```bash
sudo chown -R prefect:prefect /opt/.venv
sudo chmod -R 755 /opt/.venv/lib/python3.12/site-packages/prefect/server/ui_build
```

### 2. UI Can't Connect to API

**Issue:** "Can't connect to Server API at http://127.0.0.1:4200/api"

**Solution:**
- Add PREFECT_UI_API_URL to server.env
- Verify Nginx configuration
- Check CORS headers in Nginx configuration

### 3. Database Access Issues

**Issue:** SQLite database access errors

**Solution:**
```bash
sudo chown -R prefect:prefect /var/lib/prefect
sudo chmod 755 /var/lib/prefect
```

### 4. Service Won't Start

**Issue:** Prefect service fails to start

**Solution:**
- Check logs: `sudo journalctl -u prefect-server -f`
- Verify all directories exist and have correct permissions
- Ensure environment file exists and is readable

### 5. Nginx 502 Bad Gateway

**Issue:** Nginx returns 502 error

**Solution:**
- Verify Prefect server is running: `sudo systemctl status prefect-server`
- Check Nginx error logs: `sudo tail -f /var/log/nginx/error.log`
- Verify proxy_pass configuration points to correct address

## Verification Steps

1. **Check service status:**
   ```bash
   sudo systemctl status prefect-server
   ```

2. **Verify API access:**
   ```bash
   curl -I https://prefect.yourdomain.com/api/health
   ```

3. **Check logs:**
   ```bash
   sudo journalctl -u prefect-server -f
   sudo tail -f /var/log/nginx/error.log
   ```

4. **Test UI access by visiting:**
   ```
   https://prefect.yourdomain.com
   ```