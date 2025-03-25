import React from 'react';
import { 
  Shield, 
  Smile, 
  Zap, 
  TrendingUp, 
  AlertOctagon, 
  BarChart2 
} from 'lucide-react';

const EmotionIcon = ({ emotion }) => {
  const iconMap = {
    'joy': Smile,
    'anger': AlertOctagon,
    'sadness': TrendingUp,
    'fear': Zap,
    'surprise': BarChart2
  };

  const Icon = iconMap[emotion.toLowerCase()] || Smile;
  return <Icon className="w-6 h-6 mr-2" />;
};

const EmailCard = ({ email }) => {
  // Determine phishing risk color
  const phishingColor = 
    email.phishing.result === 'High Risk' ? 'bg-red-50 border-red-300' :
    email.phishing.result === 'Medium Risk' ? 'bg-yellow-50 border-yellow-300' :
    'bg-green-50 border-green-300';

  return (
    <div className={`
      relative overflow-hidden 
      border-2 ${phishingColor} 
      rounded-2xl shadow-lg 
      transform transition-all 
      hover:scale-105 
      p-6 space-y-4
    `}>
      <div className="absolute top-0 right-0 p-2">
        <Shield 
          className={
            email.phishing.result === 'High Risk' 
              ? 'text-red-500' 
              : email.phishing.result === 'Medium Risk' 
              ? 'text-yellow-500' 
              : 'text-green-500'
          } 
        />
      </div>

      <div className="flex items-center mb-4">
        <EmotionIcon emotion={email.emotions.primary.emotion} />
        <h2 className="text-xl font-bold text-gray-800">
          {email.emotions.primary.emotion.charAt(0).toUpperCase() + email.emotions.primary.emotion.slice(1)} Emotion
        </h2>
      </div>

      <div className="space-y-3">
        <div className="bg-white p-3 rounded-lg shadow-sm">
          <p className="text-sm text-gray-600 font-medium">
            <strong>Content Analysis:</strong>
          </p>
          <p className="text-gray-800">
            {email.analysis.content || "No analysis available"}
          </p>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div className="bg-white p-3 rounded-lg shadow-sm">
            <p className="text-xs text-gray-600 font-medium">Phishing Risk</p>
            <p className={`
              font-bold 
              ${email.phishing.result === 'High Risk' ? 'text-red-600' : 
                email.phishing.result === 'Medium Risk' ? 'text-yellow-600' : 'text-green-600'}
            `}>
              {email.phishing.result}
            </p>
            <p className="text-xs text-gray-500">
              Confidence: {email.phishing.confidence}
            </p>
          </div>

          <div className="bg-white p-3 rounded-lg shadow-sm">
            <p className="text-xs text-gray-600 font-medium">Primary Emotion</p>
            <p className="font-bold text-blue-600">
              {email.emotions.primary.emotion.charAt(0).toUpperCase() + email.emotions.primary.emotion.slice(1)}
            </p>
            <p className="text-xs text-gray-500">
              Score: {email.emotions.primary.score.toFixed(2)}
            </p>
          </div>
        </div>

        <div className="bg-white p-3 rounded-lg shadow-sm">
          <p className="text-sm text-gray-600 font-medium mb-2">Top Emotions</p>
          <div className="space-y-1">
            {email.emotions.top_emotions.map((emotion, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center">
                  <EmotionIcon emotion={emotion.emotion} />
                  <span className="text-sm text-gray-800">
                    {emotion.emotion.charAt(0).toUpperCase() + emotion.emotion.slice(1)}
                  </span>
                </div>
                <span className="text-sm text-gray-600">
                  {emotion.score.toFixed(2)}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmailCard;