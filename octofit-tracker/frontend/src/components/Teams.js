import React, { useState, useEffect } from 'react';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_CODESPACE_NAME 
    ? `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev`
    : 'http://localhost:8000';
  
  const API_ENDPOINT = `${API_BASE_URL}/api/teams/`;

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        console.log('Fetching teams from:', API_ENDPOINT);
        const response = await fetch(API_ENDPOINT);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Teams API response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        console.log('Processed teams data:', teamsData);
        
        setTeams(teamsData);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching teams:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchTeams();
  }, [API_ENDPOINT]);

  if (loading) {
    return (
      <div className="text-center">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p>Loading teams...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger" role="alert">
        <h4 className="alert-heading">Error!</h4>
        <p>Failed to load teams: {error}</p>
        <p className="mb-0">API Endpoint: {API_ENDPOINT}</p>
      </div>
    );
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="mb-1">
            <i className="fas fa-users text-success me-2"></i>Teams
          </h2>
          <small className="text-muted">API Endpoint: {API_ENDPOINT}</small>
        </div>
        <button className="btn btn-success">
          <i className="fas fa-plus me-1"></i>Create Team
        </button>
      </div>
      
      {teams.length === 0 ? (
        <div className="alert alert-info d-flex align-items-center">
          <i className="fas fa-info-circle me-2"></i>
          <div>No teams found. Create a team to get started!</div>
        </div>
      ) : (
        <div className="card shadow-sm">
          <div className="card-body p-0">
            <div className="table-responsive">
              <table className="table table-hover table-striped mb-0">
                <thead className="table-dark">
                  <tr>
                    <th scope="col">#</th>
                    <th scope="col">Team Name</th>
                    <th scope="col">Description</th>
                    <th scope="col" className="text-center">Members</th>
                    <th scope="col" className="text-center">Total Points</th>
                    <th scope="col">Captain</th>
                    <th scope="col">Created</th>
                    <th scope="col" className="text-center">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {teams.map((team, index) => (
                    <tr key={team.id || index}>
                      <th scope="row">{index + 1}</th>
                      <td>
                        <div className="d-flex align-items-center">
                          <div className="bg-success rounded-circle d-flex align-items-center justify-content-center me-3"
                               style={{width: '40px', height: '40px'}}>
                            <span className="text-white fw-bold">
                              {(team.name || 'T')[0].toUpperCase()}
                            </span>
                          </div>
                          <div>
                            <strong className="d-block">{team.name || 'Unnamed Team'}</strong>
                            <small className="text-muted">ID: {team.id || index}</small>
                          </div>
                        </div>
                      </td>
                      <td>
                        <span className="text-truncate d-inline-block" style={{maxWidth: '200px'}} title={team.description}>
                          {team.description || 'No description available'}
                        </span>
                      </td>
                      <td className="text-center">
                        <span className="badge bg-info fs-6">
                          {team.member_count || team.members?.length || 0}
                        </span>
                      </td>
                      <td className="text-center">
                        {team.total_points ? (
                          <span className="badge bg-warning fs-6">
                            {team.total_points}
                          </span>
                        ) : (
                          <span className="text-muted">-</span>
                        )}
                      </td>
                      <td>
                        {team.captain ? (
                          <span className="text-primary">
                            👑 {team.captain.username || team.captain}
                          </span>
                        ) : (
                          <span className="text-muted">No captain</span>
                        )}
                      </td>
                      <td>
                        <small className="text-muted">
                          {team.date_created || team.created_at || 'N/A'}
                        </small>
                      </td>
                      <td className="text-center">
                        <div className="btn-group btn-group-sm">
                          <button className="btn btn-outline-success btn-sm" title="View Members">
                            <i className="fas fa-eye"></i>
                          </button>
                          <button className="btn btn-outline-primary btn-sm" title="Edit Team">
                            <i className="fas fa-edit"></i>
                          </button>
                          <button className="btn btn-outline-danger btn-sm" title="Delete Team">
                            <i className="fas fa-trash"></i>
                          </button>
                        </div>
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
                  Showing {teams.length} teams
                </small>
              </div>
              <div className="col-md-6 text-end">
                <nav aria-label="Teams pagination">
                  <ul className="pagination pagination-sm justify-content-end mb-0">
                    <li className="page-item disabled">
                      <span className="page-link">Previous</span>
                    </li>
                    <li className="page-item active">
                      <span className="page-link">1</span>
                    </li>
                    <li className="page-item disabled">
                      <span className="page-link">Next</span>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Teams;