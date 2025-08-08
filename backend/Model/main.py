from text_preprocessing import text_preprocessing
from create_model import create_model
from train_model import train_model
import pickle
import re
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os


def main(csv_file_path, epochs=20, batch_size=32):
    
    print("🚀 Starting Resume Classification Pipeline...")
    print("=" * 60)
    
    try:
        # Step 1: Text preprocessing
        print("text preprocessing")
        X_train, X_test, y_train, y_test, tokenizer, label_encoder, num_classes, max_length = text_preprocessing(csv_file_path)
        print("test preprocessing done",X_train.shape, X_test.shape, y_train.shape, y_test.shape )
        # Step 2: Create model
        
        print("creating the model")
        model, summary = create_model(
            vocab_size=15000,
            max_length=max_length,
            num_classes=num_classes,
            embedding_dim=128
        )
        print("model creation is done")
        print(summary)
        
        
        print("Training Started")
        history = train_model(model, X_train, X_test, y_train, y_test, epochs, batch_size)
        print("")
        
        
        print("\n🔹 Evaluating model on test set...")
        test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
        print(f"Test Loss: {test_loss:.4f}")
        print(f"Test Accuracy: {test_accuracy:.4f}")
        
        # Step 5: Save final model
        print("\n🔹 Saving final model...")
        model.save("final_resume_model.h5")
        
        # Save model configuration
        model_config = {
            'vocab_size': 15000,
            'max_length': max_length,
            'num_classes': num_classes,
            'embedding_dim': 128,
            'test_accuracy': test_accuracy,
            'test_loss': test_loss
        }
        
        with open('model_config.pkl', 'wb') as f:
            pickle.dump(model_config, f)
        
        print("\n✅ Pipeline completed successfully!")
        print("Files saved:")
        print("  - final_resume_model.h5 (trained model)")
        print("  - best_model.h5 (best model during training)")
        print("  - tokenizer.pkl (tokenizer)")
        print("  - label_encoder.pkl (label encoder)")
        print("  - model_config.pkl (model configuration)")
        print(f"  - logs/fit/ (TensorBoard logs)")
        
        return model, history, tokenizer, label_encoder
        
    except Exception as e:
        print(f"❌ Error in pipeline: {str(e)}")
        raise e

# Example usage and prediction function

if __name__ == "__main__":
    
    csv_file ="C:\\Users\\prana\\Desktop\\Resume detector\\backend\\Model\\gpt_dataset.csv"
    
    if os.path.exists(csv_file):
        model, history, tokenizer, label_encoder = main(csv_file, epochs=20, batch_size=32)
    else:
        print(f"❌ CSV file '{csv_file}' not found!")
        print("Please make sure your resume dataset CSV file is in the same directory.")
        print("Expected columns: 'Resume' (text) and 'Category' (labels)")