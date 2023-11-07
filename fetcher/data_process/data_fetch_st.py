# This script runs the data fetcher using a single thread.
# To execute it, the following arguments are required:
# args (string): the args brings the configuration file of the project, to know the paths of the files

# Also, the data fetcher requires that the database contains at least one source stored, so it will retrieve this source information to fetch its data

import yaml
from fetch import Fetcher
from database.db import Db

import sys

sys.path.append("Questao360/")


def main(url_base, disciplina):
    # This method opens the database file and iterates through each source, to retrieve the information from the main page and its child pages. For each main page, the Fetcher object will be created and processed
    with open("config/config.yaml", "r") as f:
        cfg = yaml.safe_load(f)
    
    fetcher = Fetcher(
        (url_base, disciplina), cfg["db"]
        )
    fetcher.fetch_pages_data()


if __name__ == "__main__":
    main("https://concursos.estrategia.com/cadernos-e-simulados/cadernos/5e5cf772-4973-4b0f-ac42-29385df472e8", "Português")
