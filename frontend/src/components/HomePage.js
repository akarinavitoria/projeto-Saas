// src/components/HomePage.js
import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div>
      <h1>Lista de Academias</h1>
      <Link to="/register">Fazer Inscrição</Link>
      <Link to="/payments">Ir para Pagamentos</Link>
      <Link to="/search">Buscar Academias</Link>
    </div>
  );
}

export default HomePage;
