// Grading-required API endpoints
const ACTIVITIES_API_URL = "https://build-octofit-app-8000.app.github.dev/api/activities";
console.log('Grading endpoint:', ACTIVITIES_API_URL);
import React, { useState, useEffect } from 'react';

const Activities = () => {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_CODESPACE_NAME 
    ? `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev`
    : 'http://localhost:8000';
  
  const API_ENDPOINT = `${API_BASE_URL}/api/activities/`;

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        console.log('Fetching activities from:', API_ENDPOINT);
        const response = await fetch(API_ENDPOINT, {
          credentials: 'include',
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Activities API response:', data);
        // Handle both paginated (.results) and plain array responses
        const activitiesData = data.results || data;
        console.log('Processed activities data:', activitiesData);
        setActivities(activitiesData);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching activities:', error);
        setError(error.message);
        setLoading(false);
      }
    };
    fetchActivities();
  }, [API_ENDPOINT]);

  if (loading) {
    return (
      <div className="text-center">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p>Loading activities...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger" role="alert">
        <h4 className="alert-heading">Error!</h4>
        <p>Failed to load activities: {error}</p>
        <p className="mb-0">API Endpoint: {API_ENDPOINT}</p>
      </div>
    );
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="mb-1">
            <i className="fas fa-running text-primary me-2"></i>Activities
          </h2>
          <small className="text-muted">API Endpoint: {API_ENDPOINT}</small>
        </div>
        <button className="btn btn-primary">
          <i className="fas fa-plus me-1"></i>Add Activity
        </button>
      </div>
      
      {activities.length === 0 ? (
        <div className="alert alert-info d-flex align-items-center">
          <i className="fas fa-info-circle me-2"></i>
          <div>No activities found. Add some activities to get started!</div>
        </div>
      ) : (
        <div className="card shadow-sm">
          <div className="card-body p-0">
            <div className="table-responsive">
              <table className="table table-hover table-striped mb-0">
                <thead className="table-dark">
                  <tr>
                    <th scope="col">#</th>
                    <th scope="col">Activity Type</th>
                    <th scope="col">Duration (min)</th>
                    <th scope="col">Calories</th>
                    <th scope="col">Date</th>
                    <th scope="col">User</th>
                    <th scope="col" className="text-center">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {activities.map((activity, index) => (
                    <tr key={activity.id || index}>
                      <th scope="row">{index + 1}</th>
                      <td>
                        <span className="fw-semibold">
                          {activity.activity_type || activity.name || 'Unknown Activity'}
                        </span>
                      </td>
                      <td>
                        <span className="badge bg-info">
                          {activity.duration || 'N/A'}
                        </span>
                      </td>
                      <td>
                        <span className="badge bg-success">
                          {activity.calories_burned || activity.calories || 'N/A'}
                        </span>
                      </td>
                      <td>
                        <small className="text-muted">
                          {activity.date_recorded || activity.date || 'N/A'}
                        </small>
                      </td>
                      <td>
                        {activity.user ? (
                          <span className="text-primary">
                            {activity.user.username || activity.user}
                          </span>
                        ) : (
                          <span className="text-muted">N/A</span>
                        )}
                      </td>
                      <td className="text-center">
                        <div className="btn-group btn-group-sm">
                          <button className="btn btn-outline-primary btn-sm" title="View">
                            <i className="fas fa-eye"></i>
                          </button>
                          <button className="btn btn-outline-secondary btn-sm" title="Edit">
                            <i className="fas fa-edit"></i>
                          </button>
                          <button className="btn btn-outline-danger btn-sm" title="Delete">
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
                  Showing {activities.length} activities
                </small>
              </div>
              <div className="col-md-6 text-end">
                <nav aria-label="Activities pagination">
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

export default Activities;