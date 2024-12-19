// src/components/HomePage.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function HomePage() {
  const [gyms, setGyms] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/api/gyms')
      .then(response => setGyms(response.data))
      .catch(error => console.error('Erro ao buscar academias:', error));
  }, []);

  return (
    <div>
      <h1>Lista de Academias</h1>
      <ul>
        {gyms.map(gym => (
          <li key={gym.id}>{gym.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default HomePage;

