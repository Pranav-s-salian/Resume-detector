from flask import Flask
from flask_cors import CORS
from flask import request, jsonify
import base64
import io
from PIL import Image
import requests
from LLM.text_extraction import extract_resume_text_with_groq_for_ml, clean_for_ml_model
from Model.predicted import check_eligibility
from LLM.Feedback import generate_resume_feedback_with_groq, generate_detailed_resume_analysis_with_groq
import numpy as np  

app = Flask(__name__)
CORS(app)

def convert_numpy_types(obj):
    if isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(v) for v in obj]
    elif isinstance(obj, (np.integer, np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    else:
        return obj

@app.route('/image-capture', methods=['POST'])
def main_pipeline():
    try:
        data = request.get_json()
        
        if not data or 'image' not in data or 'category' not in data:
            return jsonify({'error': 'No image data provided, or category data provided'}), 400
        
        base64_image = data.get('image')
        category = data.get('category')
        
        print(f"Received image and category: {category}")
        
        print("Text extraction started")
        result = extract_resume_text_with_groq_for_ml(base64_image)
        print("Text extraction completed")
        
        
        if not result['success']:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
        print("Now checking the eligibility")
        text = result['ml_ready_text']
        print(text)
        clean_text = clean_for_ml_model(text)
        
        print(clean_text)
        
        eligibility_result = check_eligibility(clean_text, category)
        print(eligibility_result)
        
        if 'error' in eligibility_result:
            return jsonify({
                'success': False,
                'error': eligibility_result['error']
            }), 400
        
        
        print("Converting numpy types in eligibility result...")
        eligibility_result = convert_numpy_types(eligibility_result)
        print("Numpy conversion completed")
        
        print("Feedback in process")
        feedback_result = generate_resume_feedback_with_groq(
            eligibility_result, 
            text, 
            category
        )
        
        if 'error' in feedback_result:
            return jsonify({
                'success': False,
                'error': feedback_result['error']
            }), 400
        
        print("Generating detailed analysis...")
        # Generate detailed analysis
        detailed_analysis_result = generate_detailed_resume_analysis_with_groq(
            eligibility_result,  # This is already converted
            text,
            category
        )
        print("Detailed analysis completed")
        
        if not detailed_analysis_result['success']:
            return jsonify({
                'success': False,
                'error': detailed_analysis_result['error']
            }), 400
        
        # Build response with already converted data
        response_data = {
            'success': True,
            'extracted_text': text,
            'eligibility': {
                'eligible': eligibility_result['eligible'],
                'confidence': eligibility_result['confidence_for_target'],
                'predicted_category': eligibility_result['predicted_category'],
                'target_category': eligibility_result['target_category'],
                'score': eligibility_result['eligibility_score'],
                'all_scores': eligibility_result['all_category_scores']
            },
            'feedback': {
                'message': feedback_result['feedback'],
                'status': feedback_result['eligibility_status'],
                'confidence_display': feedback_result['confidence_score'],
                'rating': feedback_result['rating']
            },
            'detailed_analysis': detailed_analysis_result['detailed_analysis'],
            'recommendation': eligibility_result.get('recommendation', '')
        }
        
        # Final safety conversion
        final_response = convert_numpy_types(response_data)
        
        return jsonify(final_response), 200
        
    except Exception as e:
        print(f"Error in main_pipeline: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Resume analysis API is running'
    }), 200

if __name__ == '__main__':
    app.run(debug=True)