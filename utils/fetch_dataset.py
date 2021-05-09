from collections import defaultdict
from json import dumps

from boto3 import client

from cfpq_data import __version__ as cfpq_data_version
from cfpq_data.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME
from config import MAIN_FOLDER


def fetch_dataset():
    s3 = client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    dataset = defaultdict(dict)

    for graph in s3.list_objects(Bucket="cfpq-data", Prefix=cfpq_data_version)[
        "Contents"
    ]:
        graph_key = graph["Key"]
        graph_class, graph_full_name = graph_key.split("/")[1:]
        graph_name = graph_full_name.split(".")[0]
        graph_file_extension = "." + graph_full_name.split(".")[1]
        graph_archive_extension = graph_full_name.split(graph_file_extension)[1]
        dataset[graph_class][graph_name] = {
            "VersionId": s3.head_object(Bucket=BUCKET_NAME, Key=graph_key)["VersionId"],
            "FileExtension": graph_file_extension,
            "ArchiveExtension": graph_archive_extension,
        }

    return dataset


def update_dataset(dataset):
    with open(MAIN_FOLDER / "cfpq_data" / "dataset.py", "w") as fout:
        fout.write("DATASET = " + dumps(dataset, indent=4))


if __name__ == "__main__":
    dataset = fetch_dataset()
    update_dataset(dataset)
