import pickle
import re

with open("chat_classifier_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("tfidf_vectorizer.pkl", "rb") as f:
    tfidf = pickle.load(f)

#label set of tones we are assuming
label_map = {
    "romantic": "Romantic ❤️",
    "sarcastic": "Sarcastic 😜",
    "argumentative": "Argumentative 😡",
    "casual": "Casual 😁"
}

def classify_tone(df):
    df['message'] = df['message'].astype(str).str.lower().fillna('').str.strip()
    df = df[df['message'] != '']

    tfidf_input = tfidf.transform(df['message'])
    predictions = model.predict(tfidf_input)
    predicted_labels = [label_map.get(pred, "Unknown") for pred in predictions]

    updated_labels = []
    for msg, label in zip(df['message'], predicted_labels):
        if "<media omitted>" in msg:
            updated_labels.append("Informational 📂	")
        elif "http" in msg or "www." in msg:
            updated_labels.append("Informational 📂	")
        elif any(sym in msg for sym in [';', '{', '}', '==', '#', '//', '<>', '()']):
            updated_labels.append("Informational 📂	")
        else:
            updated_labels.append(label)

    df['chat_type'] = updated_labels
    return df
