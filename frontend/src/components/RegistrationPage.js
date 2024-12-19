// src/components/RegistrationPage.js
import React from 'react';

function RegistrationPage() {
  return (
    <div>
      <h1>Página de Inscrição</h1>
      <form>
        <label>Nome:</label>
        <input type="text" placeholder="Seu nome" />
        <button type="submit">Inscrever-se</button>
      </form>
    </div>
  );
}

export default RegistrationPage;
