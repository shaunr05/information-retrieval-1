import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import ast
from fetchAPI import *
from result import *
from utils.fileUtils import write_to_json
from retrieval.preprocessor import *


def backend_search(author, query):
    results = get_search_results(author)
    deduped_results = deduplicate(results)
    processed_docs = preprocess(deduped_results)
    matrix, vocab, term_to_row, doc_to_col = build_incidence_matrix(processed_docs)
    matching = retrieve_docs(query, processed_docs, matrix, term_to_row)
    save_to_csv("results.csv", matching)
    return "results.csv"


def parse_authors(authors_str):
    """Convert authors column string into a clean 'Name1, Name2' format."""
    try:
        cleaned = str(authors_str).strip().strip('"').strip("'")
        authors_list = ast.literal_eval(cleaned)
        return ", ".join(a["name"] for a in authors_list if isinstance(a, dict) and "name" in a)
    except Exception:
        return str(authors_str)


def execute_search():
    author = author_entry.get().strip()
    query = query_entry.get().strip()

    if not author:
        messagebox.showerror("Error", "Author name is required.")
        return

    try:
        csv_path = backend_search(author, query)
        df = pd.read_csv(csv_path)

        # Remove unnecessary or invalid rows
        df = df[df["Title"].notna() & (df["Title"].str.strip() != "")]
        df = df[~df["Title"].str.contains("Total citations", case=False, na=False)]

        # Clear old results
        for row in result_tree.get_children():
            result_tree.delete(row)

        # Insert new results
        for _, row in df.iterrows():
            # Convert year and citations to integers if possible
            try:
                year = int(float(row.get("Year", 0))) if not pd.isna(row.get("Year")) else ""
            except:
                year = ""
            try:
                citations = int(float(row.get("Citations", 0))) if not pd.isna(row.get("Citations")) else ""
            except:
                citations = ""

            result_tree.insert(
                "", "end",
                values=(
                    row.get("Title", ""),
                    parse_authors(row.get("Authors", "")),
                    year,
                    citations
                )
            )

        # Compute total citations
        try:
            total_citations = df["Citations"].dropna().astype(float).astype(int).sum()
        except:
            total_citations = "N/A"
        total_label.config(text=f"Total citations: {total_citations}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to execute search: {e}")


# --- GUI Setup ---
root = tk.Tk()
root.title("Publication Search")
root.geometry("950x550")

# Input frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10, padx=10, fill="x")

tk.Label(input_frame, text="Author (required):").grid(row=0, column=0, sticky="w")
author_entry = tk.Entry(input_frame, width=50)
author_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Boolean Query:").grid(row=1, column=0, sticky="w")
query_entry = tk.Entry(input_frame, width=50)
query_entry.grid(row=1, column=1, padx=5)

search_button = tk.Button(input_frame, text="Search", command=execute_search)
search_button.grid(row=0, column=2, rowspan=2, padx=10)

# Results table
columns = ("Title", "Authors", "Year", "Citations")
result_tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

# Set column headers and widths
result_tree.heading("Title", text="Title")
result_tree.heading("Authors", text="Authors")
result_tree.heading("Year", text="Year")
result_tree.heading("Citations", text="Citations")

result_tree.column("Title", width=400, anchor="w")  # wide
result_tree.column("Authors", width=250, anchor="w")  # medium
result_tree.column("Year", width=60, anchor="center")  # narrow for 4-digit year
result_tree.column("Citations", width=80, anchor="center")  # small

result_tree.pack(fill="both", expand=True, padx=10, pady=10)

# Total citations label
total_label = tk.Label(root, text="Total citations: N/A", font=("Arial", 12, "bold"))
total_label.pack(pady=5)

root.mainloop()
