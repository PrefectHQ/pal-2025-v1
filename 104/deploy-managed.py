from prefect import flow


if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/prefecthq/pacc-2025-v1.git",
        entrypoint="102/weather2-tasks.py:pipeline",
    ).deploy(
        name="my-first-managed-deployment",
        work_pool_name="managed1",
    )
