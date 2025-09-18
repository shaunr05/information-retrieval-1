# Information Retrieval Lab 1

This project allows you to fetch articles for a given author and perform boolean retrieval queries on the retrieved documents. The results are stored in a CSV file.

---

## Requirements

Before running the project, make sure Python is installed. Install the packages required for this project using:

```bash
pip install -r requirements.txt
```

## Running the code

To run the code, use the command:

```bash
py main.py fetch search [AUTHOR_NAME]
```

where [AUTHOR_NAME] is the name of the author you want to search for.

The program will then prompt you to enter the boolean query to retrieve the documents that contain the terms in the query:

```pycon
Enter query:|
```

## Output

The output of the search is stored in a file called `results.csv`. This
file contains the title, authors, year and the number of citations of the
documents that matched the boolean query. At the end of the .csv file, the
sum of all citations across all matching documents is given.

