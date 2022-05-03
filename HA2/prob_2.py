from typing import List
from sklearn.datasets import load_iris
import numpy as np
from sklearn.model_selection import train_test_split

from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

random_state = 42
np.random.seed(random_state)

class EnsembleModule:
    def __init__(self, classifiers: List) -> None:
        """
        Initialize a class item with a list of classificators
        """
        self.cassifiers = classifiers

    def fit(self, X_train, y_train):
        """
        Fit classifiers from the initialization stage
        """
        for clf in self.cassifiers:
            clf.fit(X_train, y_train)
            name = str(clf)[:35] + '...)'
            print(f'clf {name} fitted')
        print()

    def predict(self, X_test):
        """
        Get predicts from all the classifiers and return
        the most popular answers
        """
        preds = []
        for clf in self.cassifiers:
            preds.append(clf.predict(X_test))
            name = str(clf)[:35] + '...)'
            print(f'clf {name} finished prediction')
        print()
        return np.apply_along_axis(lambda a: np.argmax(np.bincount(a)), 0, preds)


if __name__ == "__main__":

    """
    1. Load iris dataset
    2. Shuffle data and divide into train / test.
    3. Prepare classifiers to initialize <StructuralPatternName> class.
    4. Train the ensemble
    """
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    classifiers = [make_pipeline(StandardScaler(), SVC(gamma='auto', random_state=random_state)),
                   make_pipeline(StandardScaler(), DecisionTreeClassifier(max_depth=5, random_state=random_state)),
                   make_pipeline(StandardScaler(), KNeighborsClassifier(8)),
                   make_pipeline(StandardScaler(), GaussianNB()),
                   make_pipeline(StandardScaler(), LogisticRegression())]
    
    ens = EnsembleModule(classifiers)

    ens.fit(X_train, y_train)

    preds = ens.predict(X_test)

acc = accuracy_score(y_test, preds)
print(f'accuracy = {acc:.2f}')
