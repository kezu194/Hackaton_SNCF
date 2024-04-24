import csv
from pathlib import Path

DATA_CSV = Path(__file__).parent.parent.parent.joinpath("assets/data.csv")


def extract_data() -> list[dict[str, str]]:
    """
    Extract data from CSV file
    :return:
    """
    with open(DATA_CSV) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        header = next(spamreader)

        list_results = []
        for row in spamreader:
            list_results.append({
                'filename': row[-1],
                'sentence': row[-3]
            })
        return list_results
