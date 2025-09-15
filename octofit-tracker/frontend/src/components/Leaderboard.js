import React, { useState, useEffect } from 'react';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_CODESPACE_NAME 
    ? `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev`
    : 'http://localhost:8000';
  
  const API_ENDPOINT = `${API_BASE_URL}/api/leaderboard/`;

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        console.log('Fetching leaderboard from:', API_ENDPOINT);
        const response = await fetch(API_ENDPOINT, {
          credentials: 'include',
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Leaderboard API response:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Processed leaderboard data:', leaderboardData);
        setLeaderboard(leaderboardData);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching leaderboard:', error);
        setError(error.message);
        setLoading(false);
      }
    };
    fetchLeaderboard();
  }, [API_ENDPOINT]);

  if (loading) {
    return (
      <div className="text-center">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p>Loading leaderboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger" role="alert">
        <h4 className="alert-heading">Error!</h4>
        <p>Failed to load leaderboard: {error}</p>
        <p className="mb-0">API Endpoint: {API_ENDPOINT}</p>
      </div>
    );
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="mb-1">
            <i className="fas fa-trophy text-warning me-2"></i>Leaderboard
          </h2>
          <small className="text-muted">API Endpoint: {API_ENDPOINT}</small>
        </div>
        <div className="btn-group">
          <button className="btn btn-outline-primary active">All Time</button>
          <button className="btn btn-outline-primary">This Month</button>
          <button className="btn btn-outline-primary">This Week</button>
        </div>
      </div>
      
      {leaderboard.length === 0 ? (
        <div className="alert alert-info d-flex align-items-center">
          <i className="fas fa-info-circle me-2"></i>
          <div>No leaderboard data found. Complete some activities to see rankings!</div>
        </div>
      ) : (
        <div className="card shadow-sm">
          <div className="card-body p-0">
            <div className="table-responsive">
              <table className="table table-hover table-striped mb-0">
                <thead className="table-dark">
                  <tr>
                    <th scope="col" className="text-center">#</th>
                    <th scope="col">Team/User</th>
                    <th scope="col" className="text-center">Total Points</th>
                    <th scope="col" className="text-center">Activities</th>
                    <th scope="col" className="text-center">Calories</th>
                    <th scope="col" className="text-center">Last Updated</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.map((entry, index) => (
                    <tr key={entry.id || index} className={
                      index === 0 ? 'table-warning' :
                      index === 1 ? 'table-secondary' :
                      index === 2 ? 'table-light' : ''
                    }>
                      <th scope="row" className="text-center">
                        <div className="d-flex align-items-center justify-content-center">
                          <span className="badge bg-dark me-2">{index + 1}</span>
                          {index === 0 && <span className="text-warning">🥇</span>}
                          {index === 1 && <span className="text-secondary">🥈</span>}
                          {index === 2 && <span className="text-muted">🥉</span>}
                        </div>
                      </th>
                      <td>
                        <div className="d-flex align-items-center">
                          <div className="bg-primary rounded-circle d-flex align-items-center justify-content-center me-3"
                               style={{width: '40px', height: '40px'}}>
                            <span className="text-white fw-bold">
                              {(entry.team?.name || entry.user?.username || entry.name || 'U')[0].toUpperCase()}
                            </span>
                          </div>
                          <div>
                            <strong className="d-block">
                              {entry.team?.name || entry.user?.username || entry.name || 'Unknown'}
                            </strong>
                            <small className="text-muted">
                              {entry.team ? 'Team' : 'Individual'}
                            </small>
                          </div>
                        </div>
                      </td>
                      <td className="text-center">
                        <span className="badge bg-primary fs-6 px-3 py-2">
                          {entry.total_points || entry.points || 0}
                        </span>
                      </td>
                      <td className="text-center">
                        <span className="fw-semibold text-info">
                          {entry.total_activities || entry.activities_count || 0}
                        </span>
                      </td>
                      <td className="text-center">
                        <span className="fw-semibold text-success">
                          {entry.total_calories || entry.calories_burned || 0}
                        </span>
                      </td>
                      <td className="text-center">
                        <small className="text-muted">
                          {entry.last_updated || entry.updated_at || 'N/A'}
                        </small>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          <div className="card-footer bg-light">
            <div className="row align-items-center">
              <div className="col-md-6">
                <small className="text-muted">
                  <i className="fas fa-users me-1"></i>
                  Showing {leaderboard.length} competitors
                </small>
              </div>
              <div className="col-md-6 text-end">
                <button className="btn btn-sm btn-outline-primary">
                  <i className="fas fa-download me-1"></i>Export Rankings
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Leaderboard;