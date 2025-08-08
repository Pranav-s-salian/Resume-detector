import React, { useState, useCallback } from 'react';
import { 
  Upload, 
  FileImage, 
  AlertCircle, 
  CheckCircle, 
  Download,
  RefreshCw,
  Eye,
  Target,
  TrendingUp,
  MessageSquare,
  Lightbulb
} from 'lucide-react';
import { AnalysisResponse, JobCategory, JOB_CATEGORIES } from '../types/api';
import { convertToBase64, validateImageFile } from '../utils/imageUtils';
import { downloadAsJSON } from '../utils/downloadUtils';
import LoadingSpinner from '../components/LoadingSpinner';
import ProgressBar from '../components/ProgressBar';
import StarRating from '../components/StarRating';

const AnalysisPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [category, setCategory] = useState<JobCategory>('frontend developer');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string>('');
  const [dragActive, setDragActive] = useState(false);
  const [step, setStep] = useState(1);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  }, []);

  const handleFileSelect = (selectedFile: File) => {
    const validation = validateImageFile(selectedFile);
    if (!validation.valid) {
      setError(validation.error || 'Invalid file');
      return;
    }

    setFile(selectedFile);
    setError('');
    
    const url = URL.createObjectURL(selectedFile);
    setPreviewUrl(url);
    setStep(2);
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const analyzeResume = async () => {
    if (!file) return;

    setLoading(true);
    setError('');
    setStep(3);

    try {
      const base64Image = await convertToBase64(file);
      
      const response = await fetch('http://localhost:5000/image-capture', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: base64Image,
          category: category
        })
      });

      const data: AnalysisResponse = await response.json();
      console.log(data)
      
      if (data.success) {
        setResult(data);
        setStep(4);
      } else {
        setError(data.error || 'Analysis failed');
        setStep(2);
      }
    } catch (err) {
      setError('Network error. Please check if the analysis service is running.');
      setStep(2);
    } finally {
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    setFile(null);
    setPreviewUrl('');
    setResult(null);
    setError('');
    setStep(1);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
  };

  const downloadResults = () => {
    if (result) {
      downloadAsJSON(result, `resume-analysis-${Date.now()}.json`);
    }
  };

  const getConfidenceColor = (confidence: number): 'green' | 'yellow' | 'red' => {
    if (confidence >= 70) return 'green';
    if (confidence >= 40) return 'yellow';
    return 'red';
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch (err) {
      console.error('Failed to copy text');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 via-gray-50 to-slate-100 pt-20">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Progress Indicator */}
        <div className="mb-8">
          <div className="flex items-center justify-center space-x-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="flex items-center">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all duration-300 ${
                  step >= i 
                    ? 'bg-blue-600 border-blue-600 text-white' 
                    : 'bg-white border-gray-300 text-gray-400'
                }`}>
                  {i}
                </div>
                {i < 4 && (
                  <div className={`w-16 h-1 mx-2 transition-all duration-300 ${
                    step > i ? 'bg-blue-600' : 'bg-gray-300'
                  }`}></div>
                )}
              </div>
            ))}
          </div>
          <div className="flex justify-center mt-4">
            <div className="text-center">
              <p className="text-sm text-gray-600">
                {step === 1 && 'Upload Resume'}
                {step === 2 && 'Select Category'}
                {step === 3 && 'Analyzing...'}
                {step === 4 && 'View Results'}
              </p>
            </div>
          </div>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center">
            <AlertCircle className="w-5 h-5 text-red-600 mr-3 flex-shrink-0" />
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {/* Step 1: File Upload */}
        {step === 1 && (
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-300/60 p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
              Upload Your Resume
            </h2>
            
            <div
              className={`border-2 border-dashed rounded-xl p-12 text-center transition-all duration-300 ${
                dragActive 
                  ? 'border-blue-500 bg-blue-50' 
                  : 'border-gray-300 hover:border-gray-400'
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Drop your resume here, or click to browse
              </h3>
              <p className="text-gray-600 mb-6">
                Supports JPG, PNG, and PDF files up to 10MB
              </p>
              
              <input
                type="file"
                accept="image/*,.pdf"
                onChange={handleFileInputChange}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors cursor-pointer"
              >
                <FileImage className="w-5 h-5 mr-2" />
                Choose File
              </label>
            </div>
          </div>
        )}

        {/* Step 2: Category Selection */}
        {step === 2 && file && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* File Preview */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-300/60 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Eye className="w-5 h-5 mr-2" />
                Resume Preview
              </h3>
              
              <div className="aspect-[3/4] bg-gray-100 rounded-lg overflow-hidden">
                <img
                  src={previewUrl}
                  alt="Resume preview"
                  className="w-full h-full object-contain"
                />
              </div>
              
              <div className="mt-4 text-sm text-gray-600">
                <p><strong>File:</strong> {file.name}</p>
                <p><strong>Size:</strong> {(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            </div>

            {/* Category Selection */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-300/60 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Target className="w-5 h-5 mr-2" />
                Target Job Category
              </h3>
              
              <div className="space-y-3 mb-6">
                {JOB_CATEGORIES.map((cat) => (
                  <label
                    key={cat}
                    className="flex items-center p-3 rounded-lg border border-gray-200 hover:bg-gray-50 cursor-pointer transition-colors"
                  >
                    <input
                      type="radio"
                      name="category"
                      value={cat}
                      checked={category === cat}
                      onChange={(e) => setCategory(e.target.value as JobCategory)}
                      className="mr-3"
                    />
                    <span className="font-medium text-gray-700 capitalize">
                      {cat.replace(/-/g, ' ')}
                    </span>
                  </label>
                ))}
              </div>
              
              <div className="flex space-x-3">
                <button
                  onClick={resetAnalysis}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Change File
                </button>
                <button
                  onClick={analyzeResume}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Analyze Resume
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Step 3: Loading */}
        {step === 3 && loading && (
          <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-300/60 p-12 text-center">
            <LoadingSpinner size="lg" text="Analyzing your resume with AI..." />
            <p className="mt-4 text-gray-600">
              This usually takes 10-30 seconds depending on resume complexity
            </p>
          </div>
        )}

        {/* Step 4: Results */}
        {step === 4 && result?.success && (
          <div className="space-y-8">
            {/* Results Header */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-300/60 p-6">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Analysis Results</h2>
                  <p className="text-gray-600">Complete AI analysis of your resume</p>
                </div>
                <div className="flex space-x-3">
                  <button
                    onClick={downloadResults}
                    className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Download
                  </button>
                  <button
                    onClick={resetAnalysis}
                    className="flex items-center px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    <RefreshCw className="w-4 h-4 mr-2" />
                    New Analysis
                  </button>
                </div>
              </div>

              {/* Eligibility Status */}
              <div className={`p-4 rounded-lg border-2 ${
                result.eligibility?.eligible 
                  ? 'bg-green-50 border-green-200' 
                  : 'bg-red-50 border-red-200'
              }`}>
                <div className="flex items-center mb-2">
                  <CheckCircle className={`w-6 h-6 mr-3 ${
                    result.eligibility?.eligible ? 'text-green-600' : 'text-red-600'
                  }`} />
                  <span className="text-lg font-semibold">
                    {result.eligibility?.eligible ? 'Eligible' : 'Not Eligible'}
                  </span>
                </div>
                <p className="text-sm text-gray-600">
                  Confidence: {result.feedback?.confidence_display} 
                  ({result.eligibility?.confidence.toFixed(1)}%)
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Extracted Text */}
              <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-300/60 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Extracted Text</h3>
                <div className="bg-gray-50 rounded-lg p-4 max-h-60 overflow-y-auto">
                  <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                    {result.extracted_text}
                  </pre>
                </div>
                <button
                  onClick={() => copyToClipboard(result.extracted_text || '')}
                  className="mt-3 text-sm text-blue-600 hover:text-blue-700"
                >
                  Copy to clipboard
                </button>
              </div>

              {/* Scores */}
              <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-300/60 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2" />
                  Category Scores
                </h3>
                
                <div className="space-y-4">
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <div className="text-3xl font-bold text-gray-900">
                      {result.eligibility?.score}/10
                    </div>
                    <div className="text-sm text-gray-600">Overall Score</div>
                  </div>
                  
                  <ProgressBar
                    value={result.eligibility?.confidence || 0}
                    label="Confidence Level"
                    color={getConfidenceColor(result.eligibility?.confidence || 0)}
                  />
                  
                  <div className="space-y-2">
                    {Object.entries(result.eligibility?.all_scores || {}).map(([cat, score]) => (
                      <div key={cat} className="flex justify-between items-center">
                        <span className="text-sm capitalize">{cat.replace(/-/g, ' ')}</span>
                        <span className="font-medium">{score.toFixed(1)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Feedback */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-300/60 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <MessageSquare className="w-5 h-5 mr-2" />
                AI Feedback
              </h3>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <StarRating rating={result.feedback?.rating || 0} />
                  <span className="text-sm text-gray-600">
                    Status: {result.feedback?.status}
                  </span>
                </div>
                
                <p className="text-gray-700 leading-relaxed">
                  {result.feedback?.message}
                </p>
              </div>
            </div>

            {/* Detailed Analysis & Recommendations */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-300/60 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Detailed Analysis</h3>
                <p className="text-gray-700 leading-relaxed">
                  {result.detailed_analysis}
                </p>
              </div>
              
              <div className="bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-300/60 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <Lightbulb className="w-5 h-5 mr-2" />
                  Recommendations
                </h3>
                <p className="text-gray-700 leading-relaxed">
                  {result.recommendation}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalysisPage;