import React from 'react';
import { Star } from 'lucide-react';

interface StarRatingProps {
  rating: number;
  maxRating?: number;
  size?: 'sm' | 'md' | 'lg';
  showValue?: boolean;
}

const StarRating: React.FC<StarRatingProps> = ({ 
  rating, 
  maxRating = 5, 
  size = 'md',
  showValue = true 
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6'
  };

  return (
    <div className="flex items-center space-x-1">
      <div className="flex space-x-1">
        {Array.from({ length: maxRating }, (_, index) => {
          const isHalf = rating - index > 0 && rating - index < 1;
          const isFull = rating > index;
          
          return (
            <div key={index} className="relative">
              <Star 
                className={`${sizeClasses[size]} text-gray-300`}
                fill="currentColor"
              />
              {(isFull || isHalf) && (
                <Star
                  className={`${sizeClasses[size]} text-yellow-400 absolute top-0 left-0`}
                  fill="currentColor"
                  style={isHalf ? { clipPath: 'inset(0 50% 0 0)' } : undefined}
                />
              )}
            </div>
          );
        })}
      </div>
      {showValue && (
  <span className="text-sm text-gray-600 ml-2">
    {isNaN(Number(rating)) ? 'N/A' : Number(rating).toFixed(1)}/{maxRating}
  </span>
)}
    </div>
  );
};

export default StarRating;