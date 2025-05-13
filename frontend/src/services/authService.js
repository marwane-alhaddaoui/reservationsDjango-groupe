const API_URL = process.env.REACT_APP_API_URL;

export async function loginUser(credentials) {
  const response = await fetch(`${API_URL}/token/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) throw new Error('Identifiants invalides');
  return response.json(); // { access, refresh }
}

export async function registerUser(data) {
  const response = await fetch(`${API_URL}/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!response.ok) throw new Error('Erreur lors de l’inscription');
  return response.json();
}
