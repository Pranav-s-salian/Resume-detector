import re
import numpy as np
from tensorflow.keras.models import load_model
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

def check_eligibility(resume_text, target_category, model_path="final_resume_model.h5", threshold=0.3):
    model = load_model(model_path)
    
    with open('tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    
    with open('label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    
    with open('model_config.pkl', 'rb') as f:
        config = pickle.load(f)

    # Clean and preprocess text
    def clean_text(text):
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text.lower()

    cleaned_text = clean_text(resume_text)

    # Tokenize and pad
    sequence = tokenizer.texts_to_sequences([cleaned_text])
    padded = pad_sequences(sequence, maxlen=config['max_length'], padding='post', truncating='post')

    # Get predictions
    predictions = model.predict(padded, verbose=0)[0]
    predicted_class_idx = np.argmax(predictions)
    predicted_category = label_encoder.inverse_transform([predicted_class_idx])[0]
    overall_confidence = predictions[predicted_class_idx]

    # Validate target category
    available_categories = list(label_encoder.classes_)
    if target_category not in available_categories:
        return {
            'error': f"Target category '{target_category}' not found. Available categories: {available_categories}"
        }

    # Get confidence for the target category
    target_class_idx = label_encoder.transform([target_category])[0]
    target_confidence = predictions[target_class_idx]

    # Determine eligibility and recommendation
    if predicted_category == target_category:
        is_eligible = True
        eligibility_score = "HIGHLY SUITABLE"
        recommendation = f"✅ RECOMMEND: Perfect match! Candidate's profile aligns well with {target_category} role."
    else:
        is_eligible = False

        if target_confidence >= 0.7:
            eligibility_score = "HIGHLY SUITABLE"
        elif target_confidence >= 0.5:
            eligibility_score = "SUITABLE"
        elif target_confidence >= 0.3:
            eligibility_score = "MODERATELY SUITABLE"
        elif target_confidence >= 0.15:
            eligibility_score = "LESS SUITABLE"
        else:
            eligibility_score = "NOT SUITABLE"

        recommendation = (
            f"✅ RECOMMEND: Good fit for {target_category}, though candidate shows stronger alignment with {predicted_category}."
            if target_confidence >= 0.5
            else f"❌ NOT RECOMMENDED: Candidate appears better suited for {predicted_category} rather than {target_category}."
        )

    return {
        'eligible': is_eligible,
        'predicted_category': predicted_category,
        'target_category': target_category,
        'confidence_for_target': round(target_confidence, 3),
        'overall_prediction_confidence': round(overall_confidence, 3),
        'eligibility_score': eligibility_score,
        'recommendation': recommendation,
        'all_category_scores': {
            category: round(predictions[i], 3)
            for i, category in enumerate(label_encoder.classes_)
        }
    }


# 👇 Add this at the bottom of predicted.py

