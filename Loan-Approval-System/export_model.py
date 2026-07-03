import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import pickle


def train_and_export(csv_path='loan_approval_dataset.csv', out_path='model_pipeline.pkl'):
    df = pd.read_csv(csv_path, skipinitialspace=True)

    # Encode categorical
    le = LabelEncoder()
    df['self_employed'] = le.fit_transform(df['self_employed'])

    # Prepare features and target (drop unused columns as in notebook)
    X = df.drop(['loan_status', 'education', 'residential_assets_value', 'loan_id'], axis=1)
    y = df['loan_status'].map({'Approved': 1, 'Rejected': 0})

    # Train/test split (optional, mostly to follow notebook pattern)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingClassifier(random_state=42)
    model.fit(X_train, y_train)

    pipeline = {
        'model': model,
        'label_encoder_self_employed': le,
        'feature_names': X.columns.tolist()
    }

    with open(out_path, 'wb') as f:
        pickle.dump(pipeline, f)

    print(f"Saved model pipeline to {out_path}")


if __name__ == '__main__':
    train_and_export()
