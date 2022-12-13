import numpy as np
import pandas as pd
import os

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

import json


class MovieModel:

    def __init__(self):
        self.dataframe = None
        self.model = None
        self.score = 0
        self.mse = 0
        self.pca = None

        self.ready = False

        self.open_db()
        self.clean_data()
        self.train_model()

        print(
            f"\n##############\n\nReady with score {self.score} and error of {self.mse}\n\n##############\n")

    def open_db(self):
        if not self.ready:
            print("Loading data")

            f = open(f'{os.getcwd()}/app/tmdb/final_db0.json')
            db = json.load(f)
            f.close()
            for num in range(1, 6):
                f = open(f'{os.getcwd()}/app/tmdb/final_db{num}.json')
                data = json.load(f)
                db = db + data
                f.close()
                print(num)

        self.dataframe = pd.DataFrame.from_dict(db)

    def clean_data(self):
        if not self.ready:
            print("Cleaning")

            self.dataframe = self.dataframe[self.dataframe["revenue"] != 0]
            self.dataframe = self.dataframe[self.dataframe["status"]
                                            == "Released"]

            avg_budget = self.dataframe['budget'].mean()
            std_budget = self.dataframe['budget'].std()
            avg_revenue = self.dataframe['revenue'].mean()
            std_revenue = self.dataframe['revenue'].std()

            self.dataframe['centered_budget'] = self.dataframe['budget'].apply(
                lambda x: (x-avg_budget)/std_budget)
            self.dataframe['centered_revenue'] = self.dataframe['revenue'].apply(
                lambda x: (x-avg_revenue)/std_revenue)
            self.dataframe['anomaly'] = self.dataframe['revenue'].apply(
                lambda x: 1 if x > (72287747*2) else 0)

            self.dataframe.dropna(subset=['revenue/day'], inplace=True)

    def train_model(self):
        if not self.ready:
            print("Training")

            X = np.array([self.dataframe['centered_budget'], self.dataframe['vote_count'],
                         self.dataframe['popularity'], self.dataframe['anomaly']]).T

            y = np.array(self.dataframe['centered_revenue']).reshape(-1, 1)

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
