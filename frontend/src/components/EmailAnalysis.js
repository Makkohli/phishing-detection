import React, { useState } from 'react';
import { fetchAndAnalyzeEmails } from '../api';
import EmailCard from './EmailCard';
import { Shield, Search, AlertTriangle } from 'lucide-react';

const EmailAnalysis = () => {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFetchEmails = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await fetchAndAnalyzeEmails();
      setEmails(data.results);
    } catch (error) {
      setError('Failed to fetch and analyze emails.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 p-8">
      <div className="max-w-4xl mx-auto bg-white shadow-2xl rounded-2xl overflow-hidden">
        <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-6 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Shield className="text-white w-10 h-10" />
            <h1 className="text-3xl font-extrabold text-white">
              AI Email Security Analysis
            </h1>
          </div>
        </div>
        
        <div className="p-6">
          <div className="flex space-x-4 mb-6">
            <button
              className="flex items-center space-x-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 px-6 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-300 shadow-lg disabled:opacity-50"
              onClick={handleFetchEmails}
              disabled={loading}
            >
              <Search className="w-5 h-5" />
              <span>{loading ? 'Analyzing Emails...' : 'Fetch & Analyze Emails'}</span>
            </button>
          </div>

          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4 flex items-center space-x-3">
              <AlertTriangle className="text-red-500 w-6 h-6" />
              <p className="text-red-700">{error}</p>
            </div>
          )}

          {emails.length > 0 ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {emails.map((email, index) => (
                <EmailCard key={index} email={email} index={index} />
              ))}
            </div>
          ) : (
            !loading && (
              <div className="text-center py-12 bg-gray-50 rounded-lg">
                <p className="text-gray-600 text-lg">
                  No emails analyzed yet. Click the button to start.
                </p>
              </div>
            )
          )}
        </div>
      </div>
    </div>
  );
};

export default EmailAnalysis;