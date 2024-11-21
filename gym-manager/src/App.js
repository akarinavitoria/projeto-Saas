// src/App.js
import React from 'react';
import Header from './components/header/header.js';
import clientsList from './pages/clients/clientsList.js';
import './styles/global.css'; // Certifique-se de criar e configurar este arquivo global de estilos.

function App() {
  return (
    <>
      <Header />
      <main>
        <clientsList/>
      </main>
    </>
  );
}

export default App;

