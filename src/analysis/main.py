"""a messy script that can help with analysis"""

import sys
from functools import reduce
from toolz.dicttoolz import update_in
import yaml
from pprint import pprint

import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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

valint = {"straight flush": 3, "win": 2, "lose": 1, "sweep": 0}
valint_binary = {"straight flush": 0, "win": 2, "lose": 1, "sweep": 0}
#valint_binary = {"straight flush": 1, "win": 1, "lose": 0, "sweep": 0}

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

        # Construct the CASE expression for detailed result categories
        correct_count = fn.Count(
            Case()
            .when(attempts.result == 'true', 1)
            .else_(None)
        )

        incorrect_count = fn.Count(
            Case()
            .when(attempts.result != 'true', 1)
            .else_(None)
        )

        predominant_result = (
            Case()
            .when((correct_count == 3) & (incorrect_count == 0), 'straight flush')
            .when((incorrect_count == 3) & (correct_count == 0), 'sweep')
            .when(correct_count == 3, 'win')
            .when(incorrect_count == 3, 'lose')
            .else_('undecided')  # Catch-all
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

    #print(data)
    #print(data.keys())

    def update_val(result, v):
        if v is None:
            v = 0

        return v + valint[result]

    def rfn2(acc, problemattempt):
        problem_name, result = problemattempt

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

        # Convert the list to integers
        int_values = [valint_binary[val] for val in scores_per_problem]

        # Create a figure and axis
        fig, ax = plt.subplots()

        cmap = mcolors.ListedColormap(["white", "orange", "blue"])

        # Visualize as a bar code using a colormap
        ax.imshow(
            [int_values],  # Wrap in another list to make it a 2D array
            cmap=cmap,
            #cmap="Greys",
            aspect='auto'
        )

        # Remove the y-axis labels
        ax.set_yticks([])

        fig.canvas.manager.set_window_title(model)

        plt.subplots_adjust(bottom=0.8)

        # Show the plot
        plt.show()
