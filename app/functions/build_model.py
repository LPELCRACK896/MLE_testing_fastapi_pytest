import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import joblib
import os
from colorama import Fore, Style, init

# Inicializa colorama para que funcione correctamente en Windows
init(autoreset=True)

class Model:
    def __init__(self, name: str) -> None:
        self.name = name
        self.X = None
        self.y = None
        self.clf = None

    def setup(self):
        url = "http://s3.amazonaws.com/assets.datacamp.com/course/Kaggle/train.csv"
        print(f"{Fore.YELLOW}[SETUP] Retrieving data{Style.RESET_ALL}")
        df = pd.read_csv(url)
        df['Age'].fillna(df['Age'].median(), inplace=True)

        self.X = df[['Age', 'Sex', 'Embarked']]
        self.y = df['Survived']
        print(f"{Fore.GREEN}[SETUP] Data loaded into X and y axis{Style.RESET_ALL}")

    def build(self):
        print(f"{Fore.YELLOW}[BUILD] Starting the build of the pipeline{Style.RESET_ALL}")
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
        print(f"{Fore.GREEN}[BUILD] Finished building the pipeline{Style.RESET_ALL}")

    def dump(self, directory_to_save_model: str):
        print(f"{Fore.YELLOW}[DUMP] Saving model to file{Style.RESET_ALL}")

        if self.clf is None:
            raise ValueError("You must build the model before dumping it.")
        
        os.makedirs(directory_to_save_model, exist_ok=True)
        
        full_model_path = os.path.join(directory_to_save_model, f"{self.name}.pkl")

        joblib.dump(self.clf, full_model_path)
        print(f"{Fore.GREEN}[DUMP] Model saved to {full_model_path}{Style.RESET_ALL}")

if __name__ == "__main__":
    model = Model("model")
    model.setup()
    model.build()
    model.dump(directory_to_save_model='./app/models/')
