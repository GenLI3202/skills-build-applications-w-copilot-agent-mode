import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary shadow">
          <div className="container-fluid d-flex align-items-center">
            <Link className="navbar-brand d-flex align-items-center" to="/">
              <img src={process.env.PUBLIC_URL + '/octofitapp-small.png'} alt="OctoFit Logo" className="app-logo me-2" />
              <span className="fw-bold">OctoFit Tracker</span>
            </Link>
            <button 
              className="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">
                    <i className="fas fa-running me-1"></i>Activities
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">
                    <i className="fas fa-trophy me-1"></i>Leaderboard
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">
                    <i className="fas fa-users me-1"></i>Teams
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/users">
                    <i className="fas fa-user me-1"></i>Users
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">
                    <i className="fas fa-dumbbell me-1"></i>Workouts
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <main className="container-fluid py-4">
          <Routes>
            <Route path="/" element={
              <div className="row justify-content-center">
                <div className="col-lg-8 col-xl-6">
                  <div className="card shadow border-0">
                    <div className="card-body text-center py-5">
                      <h1 className="display-4 fw-bold text-primary mb-3">
                        🏃‍♂️ Welcome to OctoFit Tracker
                      </h1>
                      <p className="lead text-muted mb-4">
                        Track your fitness activities, compete with teams, and achieve your goals!
                      </p>
                      <div className="row g-3">
                        <div className="col-md-4">
                          <div className="card h-100 border-primary">
                            <div className="card-body">
                              <i className="fas fa-running fa-2x text-primary mb-2"></i>
                              <h6 className="card-title">Track Activities</h6>
                              <p className="card-text small">Log your workouts and monitor progress</p>
                            </div>
                          </div>
                        </div>
                        <div className="col-md-4">
                          <div className="card h-100 border-success">
                            <div className="card-body">
                              <i className="fas fa-trophy fa-2x text-success mb-2"></i>
                              <h6 className="card-title">Compete</h6>
                              <p className="card-text small">Join teams and climb the leaderboard</p>
                            </div>
                          </div>
                        </div>
                        <div className="col-md-4">
                          <div className="card h-100 border-info">
                            <div className="card-body">
                              <i className="fas fa-chart-line fa-2x text-info mb-2"></i>
                              <h6 className="card-title">Analyze</h6>
                              <p className="card-text small">View detailed statistics and insights</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            } />
            <Route path="/activities" element={<Activities />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/users" element={<Users />} />
            <Route path="/workouts" element={<Workouts />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
