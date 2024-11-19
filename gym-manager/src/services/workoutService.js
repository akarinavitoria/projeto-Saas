import api from './api';

export const getWorkouts = async (token) => {
  const response = await api.get('/workouts', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

export const createWorkout = async (token, data) => {
  const response = await api.post('/workouts/create', data, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};
