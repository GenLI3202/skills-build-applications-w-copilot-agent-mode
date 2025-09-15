import React, { useState, useEffect } from 'react';

const Workouts = () => {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchWorkouts();
  }, []);

  const fetchWorkouts = async () => {
    try {
      const response = await fetch(`https://${process.env.CODESPACE_NAME}-8000.app.github.dev/api/workouts`);
      if (!response.ok) {
        throw new Error('Failed to fetch workouts');
      }
      const data = await response.json();
      setWorkouts(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading workouts...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="workouts">
      <h2>Workouts</h2>
      <div className="workouts-list">
        {workouts.map(workout => (
          <div key={workout.id} className="workout-card">
            <h3>{workout.name}</h3>
            <p>Description: {workout.description}</p>
            <p>Duration: {workout.duration} minutes</p>
            <p>Difficulty: {workout.difficulty}</p>
            <p>Category: {workout.category}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Workouts;