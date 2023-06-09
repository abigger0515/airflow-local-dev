import json
import pathlib
import requests
import requests.exceptions as requests_exceptions
import pendulum
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator

# DAG_ID = "download_rockets_launches"
URL = "https://ll.thespacedevs.com/2.0.0/launch/upcoming"

@task
def get_pictures():
    # Ensure directory exists
    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)
    # Download all pictures in launches.json
    with open("/tmp/launches.json") as f:
        launches = json.load(f)
        image_urls = [launch["image"] for launch in launches["results"]]
        for image_url in image_urls:
            try:
                response = requests.get(image_url)
                image_filename = image_url.split("/")[-1]
                target_file = f"/tmp/images/{image_filename}"
                with open(target_file, "wb") as f:
                    f.write(response.content)
                    print(f"Downloaded {image_url} to {target_file}")
            except requests_exceptions.MissingSchema:
                print(f"{image_url} appears to be an invalid URL.")
            except requests_exceptions.ConnectionError:
                print(f"Could not connect to {image_url}.")

@dag(
    start_date=pendulum.datetime(2023, 4, 22, tz="UTC"),
    catchup=False,
    tags=["kwliao"],
)
def download_rockets_launches():
    download_launches = BashOperator(
        task_id="download_launches",
        bash_command=f"""
            curl -o /tmp/launches.json -L '{URL}'
        """
    )

    notify = BashOperator(
        task_id="notify",
        bash_command='echo "There are now $(ls /tmp/images/ | wc -l) images."'
    )

    download_launches >> get_pictures() >> notify


download_rockets_launches()
