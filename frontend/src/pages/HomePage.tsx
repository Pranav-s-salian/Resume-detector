import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Brain, 
  Target, 
  BarChart3, 
  CheckCircle, 
  Users, 
  TrendingUp, 
  Shield,
  ArrowRight,
  Sparkles
} from 'lucide-react';

const HomePage: React.FC = () => {
  const features = [
    {
      icon: Brain,
      title: 'AI Text Extraction',
      description: 'Advanced OCR technology extracts text from resume images with 99.5% accuracy',
      color: 'text-blue-600'
    },
    {
      icon: Target,
      title: 'Multi-Category Analysis',
      description: 'Analyze across 8+ job categories including frontend, backend, ML, and cloud',
      color: 'text-green-600'
    },
    {
      icon: BarChart3,
      title: 'BI-RNN',
      description: 'Usage of bidirectional RNN Model, which is trained over 2000+ Resumes',
      color: 'text-purple-600'
    },
    {
      icon: CheckCircle,
      title: 'Actionable Feedback',
      description: 'Receive personalized recommendations to improve your resume',
      color: 'text-orange-600'
    }
  ];

  const stats = [
    { value: '10,000+', label: 'Resumes Analyzed', icon: Users },
    { value: '95%', label: 'Accuracy Rate', icon: Target },
    { value: '4.8/5', label: 'User Rating', icon: TrendingUp },
    { value: '24/7', label: 'Availability', icon: Shield }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 via-gray-50 to-slate-100">
      {/* Hero Section */}
      <section className="pt-20 pb-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-blue-50 text-blue-700 text-sm font-medium mb-6">
              <Sparkles className="w-4 h-4 mr-2" />
              AI-Powered Career Intelligence
            </div>
            
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
              Transform Your Resume with
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                {' '}AI Analysis
              </span>
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
              Get instant, professional feedback on your resume. Our advanced AI analyzes 
              your qualifications across multiple job categories and provides actionable 
              insights to boost your career prospects.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link
                to="/analyze"
                className="group inline-flex items-center px-8 py-4 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                Start Analysis
                <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map(({ value, label, icon: Icon }, index) => (
              <div
                key={label}
                className="text-center p-6 bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-300/60 hover:shadow-lg transition-all duration-300"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <Icon className="w-8 h-8 text-blue-600 mx-auto mb-3" />
                <div className="text-3xl font-bold text-gray-900 mb-1">{value}</div>
                <div className="text-sm text-gray-600">{label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Powerful Features for Career Success
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our comprehensive AI platform provides everything you need to 
              optimize your resume and advance your career.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map(({ icon: Icon, title, description, color }, index) => (
              <div
                key={title}
                className="group p-6 bg-white/80 backdrop-blur-sm rounded-2xl border border-gray-300/60 hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
                style={{ animationDelay: `${index * 150}ms` }}
              >
                <div className={`w-12 h-12 ${color} bg-gray-50 rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">{title}</h3>
                <p className="text-gray-600 leading-relaxed">{description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gradient-to-r from-gray-700 to-gray-800 rounded-3xl p-8 md:p-12 text-center text-white relative overflow-hidden">
            <div className="absolute inset-0 bg-black/20"></div>
            <div className="relative z-10">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Ready to Optimize Your Resume?
              </h2>
              <p className="text-xl mb-8 text-gray-100">
                Join thousands of professionals who have improved their careers with AI-powered insights.
              </p>
              <Link
                to="/analyze"
                className="inline-flex items-center px-8 py-4 bg-white text-gray-700 rounded-xl font-semibold hover:bg-gray-50 transition-all duration-200 shadow-lg"
              >
                Get Started Now
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;