from csv import DictWriter

from cfpq_data import graph_from_dataset
from config import MAIN_FOLDER
from fetch_dataset import fetch_dataset


def update_dataset_tables(dataset):
    for graph_class in dataset.keys():
        fieldnames = ["Graph", "#Vertices", "#Edges"]
        with open(
            MAIN_FOLDER / "docs" / "dataset" / f"{graph_class}.csv", mode="w"
        ) as csv_file:
            csv_writer = DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()

            for graph_name in dataset[graph_class]:
                graph = graph_from_dataset(graph_name)
                csv_writer.writerow(
                    dict(
                        zip(
                            fieldnames,
                            [
                                graph_name,
                                f"{graph.number_of_nodes():,}",
                                f"{graph.number_of_edges():,}",
                            ],
                        )
                    )
                )


if __name__ == "__main__":
    dataset = fetch_dataset()
    update_dataset_tables(dataset)
