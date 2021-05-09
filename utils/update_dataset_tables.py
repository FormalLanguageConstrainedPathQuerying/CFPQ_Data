from csv import DictWriter, QUOTE_MINIMAL

from cfpq_data import graph_from_dataset
from cfpq_data.dataset import DATASET
from config import MAIN_FOLDER


def update_dataset_tables(dataset):
    for graph_class in dataset.keys():
        table = list()
        fieldnames = ["Graph", "#Vertices", "#Edges"]

        for graph_name in dataset[graph_class]:
            graph = graph_from_dataset(graph_name)
            table.append(
                [
                    graph_name,
                    f"{graph.number_of_nodes():,}",
                    f"{graph.number_of_edges():,}",
                ]
            )

        table.sort(key=lambda row: int(row[2].replace(",", "")))

        with open(
            MAIN_FOLDER / "docs" / "dataset" / f"{graph_class}.csv", mode="w"
        ) as csv_file:
            csv_writer = DictWriter(
                csv_file,
                fieldnames=fieldnames,
                delimiter=";",
                quotechar='"',
                quoting=QUOTE_MINIMAL,
            )
            csv_writer.writeheader()

            for row in table:
                csv_writer.writerow(
                    dict(
                        zip(
                            fieldnames,
                            row,
                        )
                    )
                )


if __name__ == "__main__":
    update_dataset_tables(DATASET)
