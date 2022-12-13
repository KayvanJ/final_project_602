import numpy as np
import pandas as pd
import os

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

import json


class MovieModel:

    def __init__(self):
        self.model = None
        self.score = 0
        self.mse = 0
        self.pca = None

        self.ready = False

        self.start()
        print(
            f"\n##############\n\nReady with score {self.score} and error of {self.mse}\n\n##############\n")

    def start(self):
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
        print("Movies to train on", len(db))
        db = pd.DataFrame.from_dict(db)

        if not self.ready:
            print("Training")

            X_train, X_test, y_train, y_test = train_test_split(
                np.array([db['centered_budget'], db['vote_count'],
                         db['popularity'], db['anomaly']]).T,
                np.array(db['centered_revenue']).T,
                test_size=0.2, random_state=101)

            model = GradientBoostingRegressor(
                n_estimators=1000,
                learning_rate=0.1,
                max_depth=1,
                random_state=0,
                loss='squared_error'
            )

            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            self.revenue_std = db['revenue'].std()
            self.revenue_avg = db['revenue'].mean()
            self.model = model
            self.score = model.score(X_test, y_test)
            self.mse = mean_squared_error(y_true=y_test, y_pred=y_pred)
            self.ready = True

            del db

    def predict(self, features):
        pred = self.model.predict(features)[0]
        final_number = (pred * self.revenue_std) + self.revenue_avg
        return round(final_number)
