export interface AnalysisRequest {
  image: string;
  category: string;
}

export interface CategoryScores {
  [key: string]: number;
}

export interface EligibilityData {
  eligible: boolean;
  confidence: number;
  predicted_category: string;
  target_category: string;
  score: string;
  all_scores: CategoryScores;
}

export interface FeedbackData {
  message: string;
  status: string;
  confidence_display: string;
  rating: number;
}

export interface AnalysisResponse {
  success: boolean;
  extracted_text?: string;
  eligibility?: EligibilityData;
  feedback?: FeedbackData;
  detailed_analysis?: string;
  recommendation?: string;
  error?: string;
}

export const JOB_CATEGORIES = [
  'Frontend Developer',
  'Backend Developer',
  'Data Scientist',
  'Python Developer',
  'Full Stack Developer',
  'Mobile App Developer (iOS/Android)',
  'Machine Learning Engineer',
  'Cloud Engineer'
] as const;

export type JobCategory = typeof JOB_CATEGORIES[number];