import React from 'react';

export const CompanyDashboard = () => {
  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Company Dashboard</h1>
        <p>Welcome to the Skilly Industry Recruitment Portal</p>
      </header>

      <div className="dashboard-content" style={{ padding: '2rem' }}>
        <p>This is the company dashboard. Total Jobs, Applicant Counts, and Assessment activity will be summarized here.</p>
      </div>
    </div>
  );
};
