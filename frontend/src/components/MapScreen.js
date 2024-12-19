// src/components/MapScreen.js
import React, { useState } from 'react';

function MapScreen() {
  const [route, setRoute] = useState([]);

  const handleStartRoute = () => {
    // Lógica para começar a registrar a rota
  };

  const handleStopRoute = () => {
    // Lógica para parar o registro e salvar a rota
  };

  return (
    <div>
      <h1>Mapeamento de Rotas</h1>
      <button onClick={handleStartRoute}>Iniciar Rota</button>
      <button onClick={handleStopRoute}>Finalizar Rota</button>
      <div id="map" style={{ width: '100%', height: '500px' }}></div>
    </div>
  );
}

export default MapScreen;
