import csv, os, requests, argparse

from typing import List

def list_csv_files(path: str) -> List[str]: 
    """
    list_csv_files walks through all csv files in path and return the files as a list
    """
    file_list = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".csv"):
                # Print the file path
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list

def import_csv(path: str, url: str):
    """
    import_csv use the path to read the csv data, and import those data with trades API
    """
    with open(path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            response = requests.post(url, headers={"Content-Type": "application/json; charset=utf-8"}, json=row)
            if response.status_code != 200:
                # The request failed, so we can handle the error
                print("{} - Error importing trades: {}".format(response.status_code, row["id"]))
        print("{} imported".format(path))

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description="generate report")
    parser.add_argument("--api-url", dest="url", type=str, action="store", default="http://localhost:8000/trades", help="The trades API URL")
    parser.add_argument("--path", dest="path", type=str, action="store", default="", help="the csv source path")
    args = parser.parse_args()

    if args.path!= "":
        data_path = args.path
    else:
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources")

    files = list_csv_files(data_path)
    if len(files) == 0:
        print("Warning: no csv files found in path: {}".format(data_path))

    for file in files:
        import_csv(file, args.url)
