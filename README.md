from nltk import download

# Information Retrieval Lab 1

This project allows you to fetch articles for a given author and perform boolean retrieval queries on the retrieved 
documents. The results are stored in a CSV file. The results are shown to the user via the TKinter GUI.

---

## Requirements

Before running the project, make sure Python is installed. Install the packages required for this project using:

```bash
pip install -r requirements.txt 
```

also, a `.env` file is required for this with the following contents:

```dotenv
API_KEY='your_key_here'
```

and the natural language processing requires a package that can be installed with:

```bash
py -m spacy download 'en_core_web_sm'
```

## Running the code

To run the code, use the command:

```bash
py retrieval_system.py
```

The program will then open a TKinter GUI, which will utilize text boxes to prompt the user to enter the author name 
and the boolean query to retrieve the documents that contain the terms in that query.

## Output

The output of the search is stored in a file called `results.csv`. This
file contains the title, authors, year and the number of citations of the
documents that matched the boolean query. At the end of the .csv file, the
sum of all citations across all matching documents is given. This is then displayed
to the user via the TKinter GUI.

