import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const fetchAndAnalyzeEmails = async () => {
  try {
    const response = await axios.get(`${API_URL}/fetch_and_analyze`);
    return response.data;
  } catch (error) {
    console.error('Error fetching emails:', error);
    throw error;
  }
};
