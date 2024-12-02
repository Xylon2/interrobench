import sys
from functools import reduce
from toolz.dicttoolz import update_in
import yaml
from pprint import pprint

import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

import psycopg2
from pypika import Query, Table, Case, functions as fn

def helpexit():
    print("Arguments should be the run ids")

    sys.exit()

def load_config(filepath):
    with open(filepath, "r") as file:
        config = yaml.safe_load(file)

    # Ensure "debug" is always a list
    if "debug" in config:
        if config["debug"] is None:
            config["debug"] = []

    return config

def dendo(data):
    bdata = {}

    for model, details in data.items():
        # Extract the boolean values and convert them to integers (1 or 0)
        binary_vector = [1 if solved else 0 for _, solved in details['problems']]
        # Assign the binary vector to the corresponding model in the new dictionary
        bdata[model] = binary_vector

    # Convert 't'/'f' to binary (1 for pass, 0 for fail).
    binary_matrix = pd.DataFrame(bdata).T

    # Perform hierarchical clustering
    linkage_matrix = linkage(binary_matrix, method='ward')

    # Plot the dendrogram
    plt.figure(figsize=(12, 8))
    dendrogram(linkage_matrix, labels=binary_matrix.index, leaf_rotation=90)
    plt.title("Hierarchical Clustering of Students Based on Question Outcomes")
    plt.xlabel("Student")
    plt.ylabel("Distance")
    plt.tight_layout()
    plt.show()

def clustering(bdata, questions):
    binary_matrix = pd.DataFrame(
    # Replace with your actual binary (0/1) data
    [
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        # Add rows for other students...
    ],
    index=["Student A"],  # Replace with actual student IDs
    columns=questions
)

    # Define the number of clusters (this can be adjusted based on exploration)
    num_clusters = 5

    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    question_clusters = kmeans.fit_predict(question_matrix.T)

    # Add cluster labels to the questions
    question_cluster_results = pd.DataFrame({
        'Question': binary_matrix.index,
        'Cluster': question_clusters
    })

    # Group questions by their cluster to identify patterns
    clustered_questions = question_cluster_results.groupby('Cluster')['Question'].apply(list)

    # Print each cluster with its questions
    for cluster, questions_ in clustered_questions.items():
        print(f"Cluster {cluster}:")
        for question in questions_:
            print(f"  - {question}")
        print()

def main():
    # Arguments are a list of run ids
    try:
        run_ids = [int(s) for s in sys.argv[1:]]
    except ValueError:
        helpexit()

    if len(run_ids) == 0:
        helpexit()

    dbcreds = load_config("resources/credentials.yaml")["postgres-url"]

    db_conn = psycopg2.connect(dbcreds)
    cursor = db_conn.cursor()

    # We need to make a map of model names to a list of test result scores
    runs = Table("runs")
    attempts = Table("attempts")
    data = {}

    for run in run_ids:
        query = Query.from_(runs).select(runs.model_identifier, runs.final_score).where(runs.id == run)

        cursor.execute(str(query))
        model_name, final_score = cursor.fetchone()

        # Get the results

        # Construct the CASE expression for predominant_result
        predominant_result = (
            Case()
            .when(
                fn.Count(
                    Case()
                        .when(attempts.result == 'true', 1)
                        .else_(None)
                ) >= fn.Count(
                    Case()
                        .when(attempts.result != 'true', 1)
                        .else_(None)
                ),
                True
            )
            .else_(False)
            .as_('predominant_result')
        )

        # Build the query
        query = (
            Query.from_(attempts)
            .select(
                attempts.function,
                predominant_result
            )
            .where(attempts.run_id == run)
            .groupby(attempts.function)
            .orderby(attempts.function)
        )

        cursor.execute(str(query))
        problems = cursor.fetchall()

        data[model_name] = {"total_score": final_score["numerator"],
                            "problems": problems}

        # TODO problems needs to hold the list of results as 0 and 1
        

    #print(data)
    #print(data.keys())

    def update_val(result, v):
        if v is None:
            v = 0

        if result:
            return v + 1
        else:
            return v

    def rfn2(acc, problemattempt):
        problem_name, result = problemattempt
        # if problem_name == "pythagorean theorem":
        #     print(problem_name)
        #     print("  ", result)

        return update_in(acc, [problem_name], lambda v: update_val(result, v))

    def rfn1(acc, problem):
        #print(problem)
        return reduce(rfn2, problem["problems"], acc)

    # find how often each question is answered correctly and sort accordingly
    problems_solve_rate = reduce(rfn1, data.values(), {})

    problems_by_difficulty = sorted(problems_solve_rate , key=problems_solve_rate.get, reverse=True)
    
    #print(problems_by_difficulty)

    for model in data.keys():
        xs = dict(data[model]["problems"])

        scores_per_problem = [xs[prob] for prob in problems_by_difficulty]

        # Convert the boolean list to integers (True -> 1, False -> 0)
        int_values = [1 if val else 0 for val in scores_per_problem]

        # Create a figure and axis
        fig, ax = plt.subplots()

        # Visualize as a bar code using a colormap
        ax.imshow(
            [int_values],  # Wrap in another list to make it a 2D array
            cmap='Greys',  # Use a greyscale colormap
            aspect='auto'  # Stretch to fill the axis
        )

        # Remove the y-axis labels
        ax.set_yticks([])

        fig.canvas.manager.set_window_title(model)

        plt.subplots_adjust(bottom=0.8)

        # Show the plot
        plt.show()

        #dendo(data)
        #clustering(bdata)
