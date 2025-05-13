import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL;

export const fetchArtists = async () => {
  try {
    const response = await axios.get(`${API_URL}/api/artists/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching artists:', error);
    throw error;
  }
};
