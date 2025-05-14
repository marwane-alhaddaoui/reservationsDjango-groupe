// src/services/authService.js
const API_URL = process.env.REACT_APP_API_URL
/**
 * Connexion : renvoie { access, refresh }
 */
export async function loginUser({ username, password }) {
  const res = await fetch(`${API_URL}/api/token/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || 'Erreur de connexion')
  }
  return res.json()
}

/**
 * Inscription : renvoie { access, refresh }
 * (Votre endpoint /api/register/ doit renvoyer directement tokens)
 */
export async function registerUser({ username, email, password }) {
  const res = await fetch(`${API_URL}/api/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password }),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || 'Erreur lors de l’inscription')
  }
  return res.json()
}
