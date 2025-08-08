from groq import Groq
from typing import Dict, Any
import json
import numpy as np

def convert_numpy_types(obj):
    """Recursively convert numpy types to native Python types for JSON serialization"""
    try:
        import numpy as np
        
        if isinstance(obj, dict):
            return {key: convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_numpy_types(item) for item in obj]
        elif isinstance(obj, np.floating):  # Catches all numpy float types
            return float(obj)
        elif isinstance(obj, np.integer):   # Catches all numpy int types
            return int(obj)
        elif isinstance(obj, np.ndarray):   # Handle numpy arrays
            return obj.tolist()
        elif hasattr(obj, 'item'):          # For numpy scalars
            return obj.item()
        else:
            return obj
    except ImportError:
        # If numpy is not available, return as-is
        return obj

def generate_resume_feedback_with_groq(eligibility_result: Dict[str, Any], resume_text: str, target_category: str) -> Dict[str, Any]:
    """
    Generate personalized resume feedback based on eligibility check results using Groq API
    
    Args:
        eligibility_result (Dict): Result from check_eligibility function
        resume_text (str): Original resume text extracted from image
        target_category (str): Target job category applied for
        
    Returns:
        Dict[str, Any]: Personalized feedback response
    """
    client = Groq(api_key="put you api key")
    model = "meta-llama/llama-4-scout-17b-16e-instruct"
    
    try:
        # Handle error case
        if 'error' in eligibility_result:
            return {
                "success": False,
                "error": eligibility_result['error']
            }
        
        # Extract key information and convert numpy types
        is_eligible = eligibility_result.get('eligible', False)
        predicted_category = eligibility_result.get('predicted_category', '')
        confidence_for_target = float(eligibility_result.get('confidence_for_target', 0))  # Convert to float
        eligibility_score = eligibility_result.get('eligibility_score', '')
        all_scores = convert_numpy_types(eligibility_result.get('all_category_scores', {}))  # Convert nested values
        
        sorted_categories = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        if is_eligible:
            system_prompt = """
            You are a friendly and encouraging career counselor providing positive feedback to job candidates.
            The candidate's resume has been deemed suitable for their target position.
            
            Your task is to:
            1. Congratulate them warmly and positively
            2. Highlight their strengths based on the analysis
            3. Explain why their resume is good for the target role
            4. Give encouraging advice for next steps
            5. Maintain an upbeat, professional, and supportive tone
            
            Be specific about their strengths but keep the tone conversational and encouraging.
            """
        else:
            system_prompt = """
            You are a supportive and constructive career counselor providing helpful feedback to job candidates.
            The candidate's resume needs improvement for their target position.
            
            Your task is to:
            1. Be encouraging and supportive (avoid being harsh or discouraging)
            2. Acknowledge their current strengths
            3. Clearly explain areas that need improvement
            4. Provide specific, actionable advice
            5. Suggest alternative career paths if relevant
            6. End on a positive, motivational note
            
            Be constructive, specific, and maintain a helpful, encouraging tone throughout.
            """
        
        # Create detailed prompt with all the data
        user_prompt = f"""
        Please provide personalized resume feedback based on this analysis:
        
        TARGET POSITION: {target_category}
        ELIGIBILITY STATUS: {"✅ ELIGIBLE" if is_eligible else "❌ NEEDS IMPROVEMENT"}
        CONFIDENCE SCORE: {confidence_for_target:.1%}
        ELIGIBILITY RATING: {eligibility_score}
        PREDICTED BEST FIT: {predicted_category}
        
        TOP CATEGORY MATCHES:
        {chr(10).join([f"• {cat}: {score:.1%}" for cat, score in sorted_categories])}
        
        RESUME CONTENT SUMMARY:
        {resume_text[:1000]}{"..." if len(resume_text) > 1000 else ""}
        
        {"POSITIVE FEEDBACK REQUIRED:" if is_eligible else "IMPROVEMENT FEEDBACK REQUIRED:"}
        
        {f'''Please provide encouraging feedback explaining:
        - Why their resume is well-suited for {target_category}
        - What specific strengths make them a good candidate
        - What aspects of their background align well with the role
        - Positive next steps and encouragement for their job search
        - Keep the tone congratulatory and motivating''' if is_eligible else f'''Please provide constructive feedback explaining:
        - What areas of their resume need strengthening for {target_category}
        - Specific skills or experiences they should highlight more
        - How they can better align their resume with {target_category} requirements
        - Alternative career paths they might consider (since they scored higher in {predicted_category})
        - Actionable steps to improve their candidacy
        - End with encouragement and motivation'''}
        
        IMPORTANT: 
        - Write in a friendly, conversational tone
        - Be specific and reference actual details from their background
        - Keep response length moderate (200-300 words)
        - Make it personal and actionable
        """
        
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=800,
            temperature=0.7  # Slightly creative for personalized tone
        )
        
        feedback_text = response.choices[0].message.content
        
        return {
            "success": True,
            "feedback": feedback_text,
            "eligibility_status": "eligible" if is_eligible else "needs_improvement",
            "confidence_score": f"{confidence_for_target:.1%}",
            "rating": eligibility_score,
            "best_fit_category": predicted_category,
            "target_category": target_category
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to generate feedback: {str(e)}"
        }

def generate_detailed_resume_analysis_with_groq(eligibility_result: Dict[str, Any], resume_text: str, target_category: str) -> Dict[str, Any]:
    
    client = Groq(api_key="put you api key")
    model = "meta-llama/llama-4-scout-17b-16e-instruct"
    
    
    try:
        # Convert the ENTIRE eligibility_result at the very beginning
        clean_eligibility_result = convert_numpy_types(eligibility_result)
        
        is_eligible = clean_eligibility_result.get('eligible', False)
        all_scores = clean_eligibility_result.get('all_category_scores', {})
        
        system_prompt = """
        You are an expert resume analyst and career counselor. Provide detailed, actionable analysis
        of resumes with specific recommendations for improvement.
        
        Focus on:
        1. Specific strengths and weaknesses
        2. Missing keywords or skills for the target role
        3. Formatting and presentation issues
        4. Content gaps that need addressing
        5. Industry-specific recommendations
        """
        
        # Safely create scores text with error handling
        try:
            scores_text = "\n".join([f"  {category}: {float(score):.1%}" for category, score in all_scores.items()])
        except (TypeError, ValueError) as e:
            print(f"Error formatting scores: {e}")
            scores_text = str(all_scores)  # Fallback to string representation
        
        user_prompt = f"""
        Analyze this resume for a {target_category} position:
        
        ELIGIBILITY: {"SUITABLE" if is_eligible else "NEEDS IMPROVEMENT"}
        CATEGORY SCORES:
{scores_text}
        
        RESUME CONTENT:
        {resume_text}
        
        Provide detailed analysis with:
        1. STRENGTHS: What's working well
        2. WEAKNESSES: What needs improvement
        3. MISSING ELEMENTS: What's lacking for {target_category}
        4. SPECIFIC RECOMMENDATIONS: Actionable steps
        5. KEYWORD SUGGESTIONS: Important terms to include
        6. FORMATTING TIPS: How to better present information
        
        Be specific, actionable, and professional.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1200,
            temperature=0.5
        )
        
        return {
            "success": True,
            "detailed_analysis": response.choices[0].message.content,
            "eligibility_data": clean_eligibility_result  # Already converted
        }
        
    except Exception as e:
        print(f"Detailed analysis error: {str(e)}")
        print(f"Error type: {type(e)}")
        return {
            "success": False,
            "error": f"Failed to generate detailed analysis: {str(e)}"
        }