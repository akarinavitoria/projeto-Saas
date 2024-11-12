async function loginUser(email, password) {
    const response = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    
    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.token);  // Armazena o token no localStorage
        console.log('Login bem-sucedido!');
    } else {
        console.error('Erro de login:', await response.json());
    }
}

async function createWorkout(workoutData) {
    const token = localStorage.getItem('token');  // Recupera o token JWT do localStorage

    const response = await fetch('http://localhost:5000/api/workouts/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`  // Adiciona o token JWT no cabeçalho
        },
        body: JSON.stringify(workoutData)
    });

    if (response.ok) {
        const data = await response.json();
        console.log('Treino criado:', data);
    } else {
        console.error('Erro ao criar treino:', await response.json());
    }
}

async function getUserWorkouts(userId) {
    const token = localStorage.getItem('token');

    const response = await fetch(`http://localhost:5000/api/workouts/${userId}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (response.ok) {
        const data = await response.json();
        console.log('Treinos:', data.workouts);
    } else {
        console.error('Erro ao obter treinos:', await response.json());
    }
}



