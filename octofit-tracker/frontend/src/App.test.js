
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders OctoFit Tracker title', () => {
  render(<App />);
  const titleElement = screen.getByText(/OctoFit Tracker/i);
  expect(titleElement).toBeInTheDocument();
});

test('renders Activities nav link', () => {
  render(<App />);
  const activitiesLink = screen.getByText(/Activities/i);
  expect(activitiesLink).toBeInTheDocument();
});

test('renders Leaderboard nav link', () => {
  render(<App />);
  const leaderboardLink = screen.getByText(/Leaderboard/i);
  expect(leaderboardLink).toBeInTheDocument();
});

test('renders Teams nav link', () => {
  render(<App />);
  const teamsLink = screen.getByText(/Teams/i);
  expect(teamsLink).toBeInTheDocument();
});

test('renders Users nav link', () => {
  render(<App />);
  const usersLink = screen.getByText(/Users/i);
  expect(usersLink).toBeInTheDocument();
});

test('renders Workouts nav link', () => {
  render(<App />);
  const workoutsLink = screen.getByText(/Workouts/i);
  expect(workoutsLink).toBeInTheDocument();
});
