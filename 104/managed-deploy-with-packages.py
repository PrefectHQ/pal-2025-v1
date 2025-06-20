from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        "https://github.com/prefecthq/pacc-2025-v1.git",
        entrypoint="104/hello-pandas.py:my_table_flow",
    ).deploy(
        name="test-imports",
        work_pool_name="managed1",
        job_variables=dict(env=dict(EXTRA_PIP_PACKAGES="pandas")),
    )
