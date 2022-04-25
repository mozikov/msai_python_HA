from sklearn.datasets import load_iris
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
np.random.seed(42)
class SampleFacade:
    """
    1. Copy train dataset
    2. Shuffle data (don't miss the connection between X_train and y_train)
    3. Return df_share %-subsample of X_train and y_train
    """

    def __init__(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    def get_subsample(self, df_share):
        X_t = self.X_train.copy()
        y_t = self.y_train.copy()
        subsample_len = int(X_t.shape[0] * df_share)
        data_t = np.c_[X_t, y_t]
        np.random.shuffle(data_t)
        data_t = data_t[:subsample_len, :]
        X_t, y_t = data_t[:, :-1], data_t[:,-1]

        return X_t, y_t


if __name__ == "__main__":

    """
    1. Load iris dataset
    2. Shuffle data and divide into train / test.
    """
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    pattern_item = SampleFacade(X_train, y_train)
    clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
    for df_share in np.arange(0.1, 1, 0.1):
        """
        1. Preprocess curr_X_train, curr_y_train in the way you want
        2. Train Linear Regression on the subsample
        3. Save or print the score to check how df_share affects the quality
        """
        curr_X_train, curr_y_train = pattern_item.get_subsample(df_share)
        print(curr_X_train.shape, curr_y_train.shape)

        clf.fit(curr_X_train, curr_y_train)

        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f'With {df_share:.1f} gained {acc:.2f} accuracy')
