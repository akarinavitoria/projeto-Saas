import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import WorkoutList from './pages/WorkoutList';

const App = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<WorkoutList />} />
      </Routes>
    </Router>
  );
};

export default App;
