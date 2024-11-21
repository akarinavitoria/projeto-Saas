import React from 'react';
import Header from './components/Header/Header.js';
import ClientsList from 'src/pages/Clients/ClientsList';
import './styles/global.css'; // Certifique-se de criar e configurar este arquivo global de estilos.

function App() {
  return (
    <>
      <Header />
      <main>
        <ClientsList />
      </main>
    </>
  );
}

export default App;


