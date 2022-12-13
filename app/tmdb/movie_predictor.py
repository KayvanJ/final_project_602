import numpy as np
import pandas as pd
import os

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

import json


class MovieModel:

    def __init__(self):
        self.database = []
        self.dataframe = None
        self.model = None
        self.score = 0
        self.mse = 0
        self.pca = None

        self.ready = False

        self.database_len = len(self.database)

        self.open_db()
        self.clean_data()
        self.train_model()

        print(
            f"\n##############\n\nReady with score {self.score} and error of {self.mse}\n\n##############\n")

    def open_db(self):
        if not self.ready:
            print("Loading data")
            directory = f'./app/app/tmdb/final_db0.json'
            print(directory)
            f = open(directory)
            db = json.load(f)
            f.close()
            for num in range(1, 6):
                f = open(f'./app/app/tmdb/final_db{num}.json')
                data = json.load(f)
                db = db + data
                f.close()
                print(num)

        self.database = db

    def clean_data(self):
        if not self.ready:
            print("Cleaning")
            df = pd.DataFrame.from_dict(self.database)

            df = df[df["revenue"] != 0]
            df = df[df["status"] == "Released"]

            avg_budget = df['budget'].mean()
            std_budget = df['budget'].std()
            avg_revenue = df['revenue'].mean()
            std_revenue = df['revenue'].std()

            df['centered_budget'] = df['budget'].apply(
                lambda x: (x-avg_budget)/std_budget)
            df['centered_revenue'] = df['revenue'].apply(
                lambda x: (x-avg_revenue)/std_revenue)
            df['anomaly'] = df['revenue'].apply(
                lambda x: 1 if x > (72287747*2) else 0)

            df.dropna(subset=['revenue/day'], inplace=True)
            self.dataframe = df

    def train_model(self):
        if not self.ready:
            print("Training")
            df = self.dataframe

            X = np.array([df['centered_budget'], df['vote_count'],
                         df['popularity'], df['anomaly']]).T

            y = np.array(df['centered_revenue']).reshape(-1, 1)

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=101)

            model = GradientBoostingRegressor(
                n_estimators=1000,
                learning_rate=0.1,
                max_depth=1,
                random_state=0,
                loss='squared_error'
            )

            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            self.model = model
            self.score = model.score(X_test, y_test)
            self.mse = mean_squared_error(y_true=y_test, y_pred=y_pred)
            self.ready = True

    def predict(self, features):
        final_features = features
        final_number = (
            self.model.predict(final_features)[
                0] * self.dataframe['revenue'].std()
        ) + self.dataframe['revenue'].mean()

        return round(final_number)
