import httpx
from prefect import flow


@flow()
def fetch_weather(lat: float = 38.9, lon: float = -77.0):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    temps = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    forecasted_temp = float(temps.json()["hourly"]["temperature_2m"][0])
    print(f"Forecasted temp C: {forecasted_temp} degrees")
    return forecasted_temp


if __name__ == "__main__":
    """
    Additional serve options
    The serve method on flows exposes many options for the deployment. Here’s how to use some of those options:
    https://docs.prefect.io/v3/how-to-guides/deployment_infra/run-flows-in-local-processes#serve-a-flow
    The serve method on flows exposes many options for the deployment. Here’s how to use some of those options:
    cron: a keyword that allows you to set a cron string schedule for the deployment; see schedules for more advanced scheduling options
    tags: a keyword that allows you to tag this deployment and its runs for bookkeeping and filtering purposes
    description: a keyword that allows you to document what this deployment does; by default the description is set from the docstring of the flow function (if documented)
    version: a keyword that allows you to track changes to your deployment; uses a hash of the file containing the flow by default; popular options include semver tags or git commit hashes
    triggers: a keyword that allows you to define a set of conditions for when the deployment should run; see triggers for more on Prefect Events concepts
    """

    get_weather = fetch_weather
    get_weather.serve(name="deploy-3",
                        tags=["production", "weather", "api","3"], )
