# django

Ansible role to deploy Django projects.

## Project overview

This is an Ansible role that automates the deployment of Django applications.
It sets up the runtime environment, installs dependencies, configures the
application, and optionally configures nginx, supervisor, PostgreSQL, Celery,
Certbot (Let's Encrypt), and Monit.

Author: J. David Ibáñez  
Minimum Ansible version: 2.1

## Technology stack

- **Ansible** — configuration management and deployment orchestration
- **Python / Django** — the application being deployed
- **nginx** — reverse proxy and static file serving
- **Supervisor** — process control system
- **uvicorn** — ASGI server (production mode)
- **Celery** — distributed task queue worker (optional)
- **PostgreSQL** — database setup (optional)
- **Certbot** — TLS certificate provisioning via Let's Encrypt (optional)
- **Monit** — process monitoring with automatic restart (optional)
- **Node.js / npm** — frontend tooling (optional)

## Directory structure

This project follows the standard Ansible role layout:

```
.
├── defaults/main.yml      # Default configuration variables
├── handlers/main.yml      # Handlers (reload supervisor, nginx, monit)
├── library/               # Custom Ansible modules
│   ├── filter_mods.py     # Discover mods that provide a given file
│   ├── realpath.py        # Return resolved absolute path
│   └── which.py           # Locate binaries
├── meta/main.yml          # Galaxy metadata
├── tasks/                 # 20+ task files for deployment steps
├── templates/             # Jinja2 templates for generated configs
├── vars/main.yml          # Internal variables
└── AGENTS.md              # This file
```

## Deployment flow

`tasks/main.yml` imports the following task files in order:

1. **config.yml** — Merge default dictionaries with user-provided role parameters.
2. **root.yml** — Determine `django_root`. If not provided, uses the current Git working tree root.
3. **name.yml** — Determine the instance name from `django_root` basename if not provided.
4. **pull.yml** — Optionally perform a `git pull` (controlled by `django_pull`).
5. **domains.yml**, **python.yml**, **pythonpath.yml** — Compute runtime facts.
6. **dirs.yml** — Create the directory structure under `django_root`.
7. **pip.yml** — Create a Python virtual environment and install requirements.
8. **postgres.yml** — Create PostgreSQL user and database (only if `postgres` is defined).
9. **django.yml** — Generate `settings_ansible.py`, `manage.py`, `urls_ansible.py`, and run migrations.
10. **supervisor.yml** — Generate Supervisor configuration and start/stop scripts.
11. **node_modules.yml** — Run `npm install` / `npm ci` and `npm run build` if `package.json` exists (only if `django_with_node` is true).
12. **static.yml** — Run `collectstatic` (only if `nginx` is defined).
13. **nginx.yml** — Generate nginx configuration and symlink into `/etc/nginx/sites/` (only if `nginx` is defined).
14. **monit.yml** — Generate Monit configuration and symlink into `/etc/monit.d/` (only if `django_with_monit` is true).

## The "mods" system

The role supports a modular architecture. Subdirectories ("mods") under the
project root can contribute:

- `settings.py` — included into the generated `settings_ansible.py`
- `urls.py` — included into the generated `urls_ansible.py`
- `requirements.txt` — included into the generated `requirements.txt`

The custom `filter_mods` module scans a list of mod directories and returns
only those that actually contain the requested file.

## Directory layout created at runtime

Inside `django_root` the role creates:

```
${django_root}/
├── var/                   # Runtime data
│   ├── run/               # PID files and Unix sockets
│   ├── log/               # Application and supervisor logs
│   ├── static/            # Collected static files
│   ├── media/             # User-uploaded media
│   ├── sendfile/          # Internal sendfile directory
│   └── www/               # Web root (used by Certbot)
├── etc/                   # Generated configuration files
└── venv${python_version_short}/  # Python virtualenv (optional)
```

## Configuration variables

Defaults are defined in `defaults/main.yml`. Key variables include:

- `django_repo` / `django_branch` — Git repository and branch to deploy
- `django_root` — Root directory of the deployed project
- `django_project` — Django project package name (default: `project`)
- `virtualenv` — Whether to create a virtual environment (default: `true`)
- `prefix` — Alternative Python prefix path
- `pythonpath` — Extra `PYTHONPATH` to inject
- `domains` — List of allowed hostnames
- `redirects` — Map of source domains to destination domains for HTTP 301 redirects
- `cache` — Cache backend configuration
- `static_url` / `media_url` / `sendfile_url` — URL prefixes for static, media, and internal sendfile
- `django_with_monit` / `django_with_node` / `django_with_sudo` — Toggle optional features

Nested configuration dictionaries (merged with defaults in `config.yml`):

- `django_defaults` / `django` → `django_combined`
- `nginx_defaults` / `nginx` → `nginx_combined`
- `supervisor_defaults` / `supervisor` → `supervisor_combined`
- `celery_defaults` / `celery` → `celery_combined`
- `django_cert_defaults` / `django_cert` → `django_cert_combined`

## Production vs development modes

- **Production (`supervisor.daemon: true`)**
  - Runs `uvicorn` as an `fcgi-program` under Supervisor.
  - Uses a Unix socket or TCP port behind nginx.
  - Celery workers run as separate Supervisor programs.
  - Logs go to files under `var/log/`.

- **Development (`supervisor.daemon: false`)**
  - Runs Django's `runserver` directly.
  - nginx is typically not used.
  - If `django_with_node` is enabled, also starts `npm run dev`.
  - Logs go to stdout/stderr.

## Custom Ansible modules

All modules live in `library/` and are written in Python using
`ansible.module_utils.basic`:

- **filter_mods** — Given a base path, a list of directories, a filename, and a
  destination fact name, sets a fact containing only the directories where the
  file exists.
- **realpath** — Returns the resolved absolute path of a given path, optionally
  relative to a base directory.
- **which** — Returns the path to a named executable, optionally constrained to
  a base directory (useful for virtualenv/bin lookups).

## Generated files

The role auto-generates the following files inside `django_root`:

- `manage.py` — from `templates/manage.py.jinja`
- `${django_project}/settings_ansible.py` — from `templates/settings_ansible.py.jinja`
- `${django_project}/urls_ansible.py` — from `templates/urls_ansible.py.jinja`
- `etc/requirements.txt` — from `templates/requirements.txt.jinja`
- `etc/nginx.conf` — from `templates/nginx.conf`
- `etc/supervisor.conf` — from `templates/supervisor.conf`
- `etc/start.sh` / `etc/stop.sh` — from `templates/start.sh` / `templates/stop.sh`
- `etc/certbot.conf` — from `templates/certbot.conf` (HTTPS only)
- `etc/monit.conf` — from `templates/monit.conf` (Monit only)

All generated files include a header stating they are auto-generated by Ansible.

## Handlers

- `reload supervisor` — sends `HUP` to the running supervisord process
- `reload nginx` — reloads the `nginx` system service (requires `django_with_sudo`)
- `restart monit` — restarts the `monit` system service (requires `django_with_sudo`)

## Security notes

- A random 50-character `SECRET_KEY` is generated using Ansible's `password`
  lookup and persisted in `var/secret.txt`.
- HTTPS support includes optional HSTS headers.
- Uploaded files are created with permissions `0o644`.
- Internal sendfile URLs are isolated under `sendfile_url`.

## Testing and development conventions

- There are no automated unit or integration tests in this repository.
- The `.gitignore` only ignores `.*.swp` files.
- Debug mode disables auth password validators, enables the console email
  backend, and sets `INTERNAL_IPS`.
- The `TODO.txt` file tracks known improvements (e.g. nginx static compression,
  conditional Jinja2 delimiters, using native Ansible modules for git config
  and letsencrypt).

## Code style

- Task files use YAML with explicit key/value formatting.
- Comments use `#` and are written in English.
- Task names use Title Case.
- Templates use Jinja2 with explicit block markers.
- Custom modules are written in Python 3 using `pathlib.Path`.
