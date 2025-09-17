import numpy as np
import csv


def build_incidence_matrix(docs):
    vocab = sorted(set().union(*(doc["terms"] for doc in docs)))
    term_to_row = {term: i for i, term in enumerate(vocab)}
    doc_ids = [doc["id"] for doc in docs]
    doc_to_col = {doc_id: j for j, doc_id in enumerate(doc_ids)}

    matrix = np.zeros((len(vocab), len(docs)), dtype=int)
    for j, doc in enumerate(docs):
        for term in doc["terms"]:
            i = term_to_row[term]
            matrix[i, j] = 1
    return matrix, vocab, term_to_row, doc_to_col


def evaluate_query(query, matrix, term_to_row, num_docs):
    query = query.lower()

    query = query.replace("(", " ( ").replace(")", " ) ")
    tokens = query.split()

    def get_vector(term):
        return matrix[term_to_row[term]] if term in term_to_row else np.zeros(num_docs, dtype=int)

    # converts to numpy operators
    expr = []
    for tok in tokens:
        if tok == "and":
            expr.append("&")
        elif tok == "or":
            expr.append("|")
        elif tok == "not":
            expr.append("~")
        elif tok in ("(", ")"):
            expr.append(tok)
        else:
            expr.append(f"get_vector('{tok}')")

    expr_str = " ".join(expr)
    result = eval(expr_str, {"get_vector": get_vector, "np": np})
    return result


def retrieve_docs(query, docs, matrix, term_to_row):
    num_docs = len(docs)
    result_vec = evaluate_query(query, matrix, term_to_row, num_docs)
    matching_indices = [i for i, val in enumerate(result_vec) if val == 1]
    return [docs[i] for i in matching_indices]


def save_to_csv(filename, papers):
    fieldnames = ["Title", "Authors", "Year", "Citations"]
    total_citations = 0

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for p in papers:
            citations = int(p.get("citations", 0) or 0)
            total_citations += citations

            writer.writerow({
                "Title": p.get("title", ""),
                "Authors": p.get("authors", ""),
                "Year": p.get("year", ""),
                "Citations": p.get("citations", "")
            })

        f.write(f"Total citations; {total_citations}\n")

# # example data
# docs = [
#     {"id": 0, "title": "Deep Learning for NLP",
#      "authors": "Author A", "year": "2018", "citations": 150,
#      "terms": {"deep", "learn", "nlp"}},
#
#     {"id": 1, "title": "Convolutional Neural Networks",
#      "authors": "Author B", "year": "2015", "citations": 200,
#      "terms": {"convolutional", "neural", "network"}},
#
#     {"id": 2, "title": "Probabilistic Models in Machine Learning",
#      "authors": "Author C", "year": "2012", "citations": 120,
#      "terms": {"probabilistic", "model", "machine", "learn"}},
# ]
#
# # here is how I arranged it to work
#
# # it builds the incidence matrix
# matrix, vocab, term_to_row, doc_to_col = build_incidence_matrix(docs)
#
# # then runs the query which also supports parentheses
# query = "deep AND (nlp OR probabilistic)"
# matching = retrieve_docs(query, docs, matrix, term_to_row)
#
# # saves results to a csv we can use for the frontend (we can remove the print later)
# save_to_csv("results.csv", matching)
# print(f"Saved {len(matching)} matching docs to results.csv")