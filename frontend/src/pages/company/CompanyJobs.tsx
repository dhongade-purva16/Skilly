import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import apiClient from '../../services/apiClient';

export const CompanyJobs = () => {
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await apiClient.get('/company/jobs');
        setJobs(response.data);
      } catch (error) {
        console.error('Failed to fetch jobs', error);
      } finally {
        setLoading(false);
      }
    };
    fetchJobs();
  }, []);

  if (loading) return <div>Loading jobs...</div>;

  return (
    <div className="page-container">
      <header className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1>Company Jobs</h1>
          <p>Manage your recruitment jobs and internships</p>
        </div>
        <Link to="/company/jobs/new" className="btn btn-primary">Create New Job</Link>
      </header>

      <div className="content-section" style={{ padding: '2rem' }}>
        {jobs.length === 0 ? (
          <p>No jobs found. Create one to get started.</p>
        ) : (
          <div className="jobs-list" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {jobs.map(job => (
              <div key={job.id} className="card" style={{ padding: '1rem', border: '1px solid #ccc', borderRadius: '8px' }}>
                <h3>{job.title}</h3>
                <p>Status: {job.status}</p>
                <p>Assessment Required: {job.assessment_required ? 'Yes' : 'No'}</p>
                <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem' }}>
                  <Link to={`/company/jobs/${job.id}`} className="btn btn-secondary">View Details</Link>
                  <Link to={`/company/jobs/${job.id}/applicants`} className="btn btn-secondary">View Applicants</Link>
                  {job.assessment_required && (
                    <Link to={`/company/jobs/${job.id}/assessment`} className="btn btn-secondary">Manage Assessment</Link>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
