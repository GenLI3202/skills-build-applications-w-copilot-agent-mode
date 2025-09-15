import React, { useState, useEffect } from 'react';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_CODESPACE_NAME 
    ? `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev`
    : 'http://localhost:8000';
  
  const API_ENDPOINT = `${API_BASE_URL}/api/users/`;

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        console.log('Fetching users from:', API_ENDPOINT);
        const response = await fetch(API_ENDPOINT);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Users API response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const usersData = data.results || data;
        console.log('Processed users data:', usersData);
        
        setUsers(usersData);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching users:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchUsers();
  }, [API_ENDPOINT]);

  if (loading) {
    return (
      <div className="text-center">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p>Loading users...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger" role="alert">
        <h4 className="alert-heading">Error!</h4>
        <p>Failed to load users: {error}</p>
        <p className="mb-0">API Endpoint: {API_ENDPOINT}</p>
      </div>
    );
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="mb-1">
            <i className="fas fa-user text-info me-2"></i>Users
          </h2>
          <small className="text-muted">API Endpoint: {API_ENDPOINT}</small>
        </div>
        <button className="btn btn-info">
          <i className="fas fa-user-plus me-1"></i>Add User
        </button>
      </div>
      
      {users.length === 0 ? (
        <div className="alert alert-info d-flex align-items-center">
          <i className="fas fa-info-circle me-2"></i>
          <div>No users found. Register some users to get started!</div>
        </div>
      ) : (
        <div className="card shadow-sm">
          <div className="card-body p-0">
            <div className="table-responsive">
              <table className="table table-hover table-striped mb-0">
                <thead className="table-dark">
                  <tr>
                    <th scope="col">#</th>
                    <th scope="col">User</th>
                    <th scope="col">Email</th>
                    <th scope="col" className="text-center">Status</th>
                    <th scope="col" className="text-center">Activities</th>
                    <th scope="col" className="text-center">Calories</th>
                    <th scope="col">Team</th>
                    <th scope="col">Joined</th>
                    <th scope="col" className="text-center">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user, index) => (
                    <tr key={user.id || index}>
                      <th scope="row">{index + 1}</th>
                      <td>
                        <div className="d-flex align-items-center">
                          <div className="bg-info rounded-circle d-flex align-items-center justify-content-center me-3"
                               style={{width: '40px', height: '40px'}}>
                            <span className="text-white fw-bold">
                              {(user.username || user.first_name || 'U')[0].toUpperCase()}
                            </span>
                          </div>
                          <div>
                            <strong className="d-block">{user.username || 'Unknown User'}</strong>
                            <small className="text-muted">
                              {user.first_name && user.last_name 
                                ? `${user.first_name} ${user.last_name}`
                                : ''}
                            </small>
                          </div>
                        </div>
                      </td>
                      <td>
                        <span className="text-truncate d-inline-block" style={{maxWidth: '150px'}} title={user.email}>
                          {user.email || 'N/A'}
                        </span>
                      </td>
                      <td className="text-center">
                        <span className={`badge ${user.is_active ? 'bg-success' : 'bg-danger'}`}>
                          {user.is_active ? 'Active' : 'Inactive'}
                        </span>
                        {user.is_staff && (
                          <div className="mt-1">
                            <span className="badge bg-warning">Staff</span>
                          </div>
                        )}
                        {user.is_superuser && (
                          <div className="mt-1">
                            <span className="badge bg-danger">Admin</span>
                          </div>
                        )}
                      </td>
                      <td className="text-center">
                        <span className="badge bg-primary">
                          {user.total_activities || 0}
                        </span>
                      </td>
                      <td className="text-center">
                        <span className="badge bg-success">
                          {user.total_calories || 0}
                        </span>
                      </td>
                      <td>
                        {user.team ? (
                          <span className="badge bg-secondary">
                            {user.team.name || user.team}
                          </span>
                        ) : (
                          <span className="text-muted">No team</span>
                        )}
                      </td>
                      <td>
                        <small className="text-muted">
                          {user.date_joined || user.created_at || 'N/A'}
                        </small>
                      </td>
                      <td className="text-center">
                        <div className="btn-group btn-group-sm">
                          <button className="btn btn-outline-info btn-sm" title="View Profile">
                            <i className="fas fa-eye"></i>
                          </button>
                          <button className="btn btn-outline-primary btn-sm" title="Edit User">
                            <i className="fas fa-edit"></i>
                          </button>
                          <button className="btn btn-outline-danger btn-sm" title="Delete User">
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
                  Showing {users.length} users
                </small>
              </div>
              <div className="col-md-6 text-end">
                <nav aria-label="Users pagination">
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

export default Users;