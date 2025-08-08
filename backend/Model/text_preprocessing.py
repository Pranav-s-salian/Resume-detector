import pandas as pd
import numpy as np
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pickle



def text_preprocessing(csv_file_path):
   
    print("Loading dataset...")
    df = pd.read_csv(csv_file_path)
    print(f"Dataset shape: {df.shape}")
    print("\nClass distribution:")
    print(df['Category'].value_counts())
    
    def clean_text(text):
        
        if pd.isna(text):
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '', text)
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Convert to lowercase
        text = text.lower()
        
        return text
    
    print("\n🔹 Cleaning text data...")
    df['cleaned_resume'] = df['Resume'].apply(clean_text)
    
    # Remove empty rows after cleaning
    df = df[df['cleaned_resume'].str.len() > 0]
    print(f"Dataset shape after cleaning: {df.shape}")
    
    print("\n🔹 Encoding labels...")
    label_encoder = LabelEncoder()
    df['encoded_label'] = label_encoder.fit_transform(df['Category'])
    num_classes = len(label_encoder.classes_)
    print(f"Number of classes: {num_classes}")
    print("Classes:", label_encoder.classes_)
    
    print("\n🔹 Tokenizing and padding sequences...")
    # Initialize tokenizer
    tokenizer = Tokenizer(num_words=15000, oov_token="<OOV>")
    tokenizer.fit_on_texts(df['cleaned_resume'])
    
    # Convert texts to sequences
    sequences = tokenizer.texts_to_sequences(df['cleaned_resume'])
    
    # Calculate optimal max length (95th percentile)
    sequence_lengths = [len(seq) for seq in sequences]
    max_length = int(np.percentile(sequence_lengths, 95))
    max_length = min(max_length, 500)  # Cap at 500 for memory efficiency
    print(f"Max sequence length: {max_length}")
    
    # Pad sequences
    padded = pad_sequences(sequences, maxlen=max_length, padding='post', truncating='post')
    
    print("\n🔹 Splitting data...")
    X = padded
    y = df['encoded_label']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    
    print(f"Training set shape: {X_train.shape}")
    print(f"Test set shape: {X_test.shape}")
    
    # Save tokenizer and label encoder
    with open('tokenizer.pkl', 'wb') as f:
        pickle.dump(tokenizer, f)
    
    with open('label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    
    return X_train, X_test, y_train, y_test, tokenizer, label_encoder, num_classes, max_length


