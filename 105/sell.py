from prefect import flow


@flow(log_prints=True)
def sell(ticker: str = "AAPL"):
    """Sell securities"""
    print("Sold securities!")
    return ticker


if __name__ == "__main__":
    sell.from_source(
        source="https://github.com/prefecthq/pacc-2025-v1.git",
        entrypoint="105/sell.py:sell",
    ).deploy(
        name="selling-deployment",
        work_pool_name="managed1",
    )
