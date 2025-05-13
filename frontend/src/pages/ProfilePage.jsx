// src/pages/ProfilePage.jsx
import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../context/AuthContext';

const API = process.env.REACT_APP_API_URL;

export default function ProfilePage() {
  const { accessToken } = useContext(AuthContext);
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!accessToken) return;
    fetch(`${API}/api/profile/`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error('Impossible de charger le profil');
        return res.json();
      })
      .then((data) => setProfile(data))
      .catch((err) => setError(err.message));
  }, [accessToken]);

  if (error) return <p style={{ color: 'red' }}>{error}</p>;
  if (!profile) return <p>Chargement du profil…</p>;

  return (
    <div className="profile-page">
      <h1>Mon profil</h1>
      <ul>
        <li><strong>Username :</strong> {profile.username}</li>
        <li><strong>Email :</strong> {profile.email}</li>
        <li><strong>Prénom :</strong> {profile.first_name || '-'}</li>
        <li><strong>Nom :</strong> {profile.last_name || '-'}</li>
      </ul>
    </div>
  );
}
