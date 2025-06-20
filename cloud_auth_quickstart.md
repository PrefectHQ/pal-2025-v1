# Install and authentication Quickstart

## 1. [Log in to Cloud from your browser](https://app.prefect.cloud/)

Much of Prefect's functionality is backed by an API. Sign up for a forever free Prefect Cloud account or accept your organization's invite to join their Prefect Cloud account. To access Prefect's UI, head to our [SSO login page](https://app.prefect.cloud/auth/discovery) to sign in to Prefect Cloud.

⚠️‼️ IF your organization has set up SSO and you are using your organization's account, please click `Sign in with SSO` to avoid creating a duplicate account tied to your organization email.

<img src="images/sso_login_button.png" width="300"/>

## 2. Ensure you have Prefect installed in your virtual environment

Please see the [this guide](https://gist.github.com/discdiver/0bb3bf96f02c182f96d45278f9564551) if you need assistance creating a Python virtual environment.

```bash
pip install -U prefect 
```

For more info see the [Install docs](https://docs.prefect.io/latest/getting-started/installation/)

Check that you have a recent Prefect version:

```bash
prefect version
```

<img src="images/output_prefect_version.png" width="300"/>

## 3. [Authenticate your CLI to Prefect Cloud](https://docs.prefect.io/latest/cloud/connecting/#log-into-prefect-cloud-from-a-terminal)

```bash
prefect cloud login
```

Select **Log in with a web browser**

![Alt text](images/login_with_wbrowser.png)

Alternatively, manually login with API key as shown in the[docs](https://docs.prefect.io/latest/manage/cloud/manage-users/api-keys#create-an-api-key).

Then select the desired workspace from list if there is more than one, press enter if there is only one.

## 4. Run a [hello world flow](hello_world_flow.py) and verify that you can see the flow run in the UI

```python
from prefect import flow


@flow(log_prints=True)
def hello_world():
    print("Hello world!")

if __name__ == "__main__":
    hello_world()
```

Click on the link listed in the flow run logs:

```bash
(base) ➜  prefect-pacc-2024 git:(main) python hello_world_flow.py 
09:23:52.648 | INFO    | prefect.engine - Created flow run 'noisy-frog' for flow 'hello-world'
09:23:52.650 | INFO    | Flow run 'noisy-frog' - View at https://app.prefect.cloud/account/9b649228-0419-40e1-9e0d-44954b5c0ab6/workspace/f7fe0729-5a91-40a4-a800-4bb8c5b6a6f5/flow-runs/flow-run/ea412cbd-9878-41e6-9e36-0be279230875
09:23:52.867 | INFO    | Flow run 'noisy-frog' - Hello world!
09:23:53.393 | INFO    | Flow run 'noisy-frog' - Finished in state Completed()
```

In the UI, click on the *Runs* tab and you should see a flow run with a randomly generated adjective-animal name.

🎉 Congrats! You're ready to dive in and learn Prefect!

## [Prefect Profiles](https://docs.prefect.io/latest/guides/settings/#configuration-profiles)

Prefect allows you to persist settings instead of setting an environment variable each time you open a new shell. Settings are persisted to *profiles*.

One profile is always active.

When you authenticated your CLI, that information was saved to your active profile.

### Interacting with profiles

Create a profile:

```bash
prefect profile create staging
```

Switch active profile:

```bash
prefect profile use staging
```

List profile:

```bash
prefect profile ls
```

Inspect the currently active profile:

```bash
prefect profile inspect
```

Profiles are stored by default in your PREFECT_HOME directory:

```bash
cat ~/.prefect/profiles.toml
```

Example `profiles.toml` file:

```toml
active = "default"

[profiles.local]
PREFECT_API_URL = "http://127.0.0.1:4200/api"

[profiles.default]
PREFECT_API_KEY = "pnu_----replace-me----"
PREFECT_API_URL = "https://api.prefect.cloud/api/accounts/--replace-me--/workspaces/--replace-me--"

[profiles.staging]
PREFECT_API_KEY = "pnu_----replace-me----"
PREFECT_API_URL = "https://api.prefect.cloud/api/accounts/--replace-me--/workspaces/--staging-workspace-replace-me--"
PREFECT_LOGGING_LEVEL = "DEBUG"

[profiles.n]
PREFECT_API_KEY = "pnu_----replace-me----"
PREFECT_API_URL = "https://api.prefect.cloud/api/accounts/--replace-me--/workspaces/--n-workspace-replace-me--"
```
