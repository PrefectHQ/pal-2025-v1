# Module 101: Prefect Basics

This module covers the fundamentals of Prefect workflows, including setting up your development environment and basic flow creation.

## Initial Setup

### 1. Configure Prefect Profiles

Create a profile configuration in `~/.prefect/profiles.toml`:

```toml
active = "dev"
[profiles.default]
PREFECT_API_URL = "http://127.0.0.1:4200/api"
PREFECT_DEFAULT_WORK_POOL_NAME = "default-pool"
PREFECT_LOGGING_LEVEL = "DEBUG"

[profiles.dev]
PREFECT_API_URL = "http://127.0.0.1:4200/api"
PREFECT_DEFAULT_WORK_POOL_NAME = "dev-pool"
PREFECT_LOGGING_LEVEL = "DEBUG"
PREFECT_UI_URL = "http://127.0.0.1:4200"
```

#### Profile Management Commands

1. Create a new profile:
```bash
prefect profile create my_cloud_profile
```

2. Inspect profile settings:
```bash
prefect profile inspect my_cloud_profile
```

3. Switch between profiles:
```bash
prefect profile use my_cloud_profile
```

4. List available profiles:
```bash
prefect profile ls
```

Verify your profiles:
```bash
prefect profile ls
```

### 2. Start Prefect Server

Start the local Prefect server:
```bash
prefect server start
```

This will start:
- Prefect API at http://127.0.0.1:4200/api
- Prefect UI Dashboard at http://127.0.0.1:4200
- API Documentation at http://127.0.0.1:4200/docs

## Examples

1. **Basic Weather Flow**
   - `weather1-bare.py`: Basic weather API call
   - `weather1-flow.py`: Weather API call as a Prefect flow
   - `weather1-serve.py`: Serving the weather flow
   - `weather1-serve-params.py`: Weather flow with parameters
   - `weather1-serve-schedule.py`: Scheduled weather flow

2. **Multiple Flows**
   - `serve-two-flows.py`: Running multiple flows in one server
   - `serve-two-flows-scheduled.py`: Multiple scheduled flows

## Running the Examples

1. Make sure the Prefect server is running:
```bash
prefect server start
```

2. Run any example:
```bash
python weather1-flow.py
```

3. View the flow runs in the Prefect UI at http://127.0.0.1:4200

## Key Concepts

- Development environment setup
- Profile configuration
- Server management
- Basic flow creation and decoration
- Flow parameters and configuration
- Flow scheduling
- Multiple flow management
- Flow serving and monitoring 