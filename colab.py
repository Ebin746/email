# 1) Imports
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 2) Load Dataset
df = pd.read_csv('spam_ham_dataset.csv')
df = df[['text', 'label_num']]        # Select relevant columns
df.columns = ['text', 'label']        # Rename for simplicity
df.dropna(inplace=True)               # Remove any missing rows

# 3) Visualize Class Distribution
sns.countplot(data=df, x='label')
plt.title("0 = Ham, 1 = Spam")
plt.show()

# 4) Clean the Text
def clean_text(text):
    text = text.lower()                         # Lowercase
    text = re.sub(r'\W', ' ', text)             # Remove special characters
    text = re.sub(r'\s+', ' ', text)            # Remove extra spaces
    return text.strip()

df['cleaned_text'] = df['text'].apply(clean_text)

# 5) TF-IDF Vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['cleaned_text'])
y = df['label']

# 6) Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# 7) Train Naive Bayes Model
model = MultinomialNB()
model.fit(X_train, y_train)

# 8) Evaluate Model
y_pred = model.predict(X_test)
print("\n🔍 Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\n📄 Classification Report:\n", classification_report(y_test, y_pred))

# 9) Save Model & Vectorizer
joblib.dump(model, 'spam_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("\n✅ Model and vectorizer saved successfully.")
