import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import joblib
import os

class Model:
    def __init__(self, name: str) -> None:
        self.name = name
        self.X = None
        self.y = None
        self.clf = None

    def setup(self):
        url = "http://s3.amazonaws.com/assets.datacamp.com/course/Kaggle/train.csv"
        df = pd.read_csv(url)
        df['Age'].fillna(df['Age'].median(), inplace=True)

        self.X = df[['Age', 'Sex', 'Embarked']]
        self.y = df['Survived']

    def build(self):
        if self.X is None or self.y is None:
            raise ValueError("You must call the setup method before building the model.")

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', 'passthrough', ['Age']),
                ('cat', OneHotEncoder(), ['Sex', 'Embarked'])
            ])

        self.clf = Pipeline(steps=[('preprocessor', preprocessor),
                                   ('classifier', LogisticRegression(max_iter=200))])

        self.clf.fit(self.X, self.y)

    def dump(self, directory_to_save_model: str):

        if self.clf is None:
            raise ValueError("You must build the model before dumping it.")
        
        os.makedirs(directory_to_save_model, exist_ok=True)
        
        full_model_path = os.path.join(directory_to_save_model, f"{self.name}.pkl")

        joblib.dump(self.clf, full_model_path)
        print(f"Model saved to {full_model_path}")

if __name__ == "__main__":
    model = Model("model")
    model.setup()
    model.build()
    model.dump(directory_to_save_model='./app/models/')
