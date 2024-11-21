// src/App.js
import React from 'react';
import Header from './components/header/heade';
import ClientsList from './pages/clients/clientsList';
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

