import numpy as np
import pandas as pd
from datetime import datetime
import os

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import cpi

import json

cpi.update()


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

        print(f"Ready with score {self.score} and error of {self.mse}")

    def open_db(self):
        print(self.ready)
        if not self.ready:
            print("loading")
            f = open(f'{os.getcwd()}/app/tmdb/final_db.json')
            db = json.load(f)
            f.close()

        self.database = db

    def clean_data(self):
        if not self.ready:
            print("cleaning")
            df = pd.DataFrame.from_dict(self.database)

            df['release_date'] = df['release_date'].apply(
                lambda x: tryconvert(x))
            df['count_g'] = df['genres'].apply(lambda x: len(x))
            df['cast%M'] = df['credits'].apply(lambda x: sum(
                i['gender'] == 2 for i in x['cast'])/len(x['cast']) if len(x['cast']) != 0 else np.nan)
            df['crew%M'] = df['credits'].apply(lambda x: sum(
                i['gender'] == 2 for i in x['crew'])/len(x['crew']) if len(x['crew']) != 0 else np.nan)
            df['#cast'] = df['credits'].apply(lambda x: len(x['cast']))
            df['#crew'] = df['credits'].apply(lambda x: len(x['cast']))
            df['days_out'] = df['release_date'].apply(
                lambda x: (datetime.now() - x).days)

            for i, row in df.iterrows():
                temp_revenue = row['revenue']
                df.loc[i, 'revenue/day'] = temp_revenue / row['days_out']

            df['genre1'] = df['genres'].apply(
                lambda x: x[0]['name'] if x else "None")
            df['genre1id'] = df['genres'].apply(
                lambda x: x[0]['id'] if x else 0)

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
            print("training")
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


def tryconvert(date):
    try:
        return datetime.strptime(date, '%Y-%m-%d') if date != '' else np.nan
    except:
        return np.nan
