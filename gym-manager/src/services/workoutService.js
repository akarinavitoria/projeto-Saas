import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/api'; // Altere para sua URL backend

export const getWorkouts = async (token) => {
  const response = await axios.get(`${API_URL}/workouts`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return response.data;
};
