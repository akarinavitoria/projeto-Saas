import React from 'react';

const WorkoutCard = ({ name, duration, date }) => {
  return (
    <div style={{ border: '1px solid #ccc', padding: '1rem', margin: '0.5rem 0' }}>
      <h3>{name}</h3>
      <p>Duração: {duration} minutos</p>
      <p>Data: {new Date(date).toLocaleDateString()}</p>
    </div>
  );
};

export default WorkoutCard;
