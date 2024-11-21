import React, { useState, useEffect } from 'react';
import './clientsList.css';
import axios from 'axios';

function ClientsList() {
  const [clients, setClients] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/clients') // Rota da API
      .then(response => setClients(response.data))
      .catch(error => console.error('Erro ao buscar clientes:', error));
  }, []);

  return (
    <div className="clients-list">
      <h2>Clientes</h2>
      <ul>
        {clients.map(client => (
          <li key={client.id}>
            {client.name} - {client.email}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ClientsList;
