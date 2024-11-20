import React, { useEffect, useState } from 'react';
import { getWorkouts } from '../services/workoutService';
import WorkoutCard from '../components/WorkoutCard';

const WorkoutList = () => {
  const [workouts, setWorkouts] = useState([]);

  useEffect(() => {
    const fetchWorkouts = async () => {
      try {
        const token = localStorage.getItem('access_token'); // Obtém o token
        const data = await getWorkouts(token);
        setWorkouts(data);
      } catch (error) {
        console.error('Erro ao buscar treinos:', error);
      }
    };

    fetchWorkouts();
  }, []);

  return (
    <div>
      <h1>Lista de Treinos</h1>
      {workouts.length > 0 ? (
        workouts.map((workout) => (
          <WorkoutCard key={workout.id} {...workout} />
        ))
      ) : (
        <p>Carregando treinos...</p>
      )}
    </div>
  );
};

export default WorkoutList;
