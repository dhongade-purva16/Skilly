import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import apiClient from '../../services/apiClient';

export const StudentJobs = () => {
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await apiClient.get('/student/jobs');
        setJobs(response.data);
      } catch (error) {
        console.error('Failed to fetch jobs', error);
      } finally {
        setLoading(false);
      }
    };
    fetchJobs();
  }, []);

  const handleApply = async (jobId: number) => {
    try {
      await apiClient.post(`/student/jobs/${jobId}/apply`);
      alert('Successfully applied!');
    } catch (error: any) {
      if (error.response?.status === 409) {
        alert('You have already applied to this job.');
      } else {
        alert('Failed to apply. Please try again later.');
      }
    }
  };

  if (loading) return <div>Loading jobs...</div>;

  return (
    <div className="page-container">
      <header className="page-header">
        <h1>Available Jobs & Internships</h1>
        <p>Discover opportunities from target companies</p>
      </header>

      <div className="content-section" style={{ padding: '2rem' }}>
        {jobs.length === 0 ? (
          <p>No active jobs available at the moment.</p>
        ) : (
          <div className="jobs-list" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {jobs.map(job => (
              <div key={job.id} className="card" style={{ padding: '1.5rem', border: '1px solid #ccc', borderRadius: '8px' }}>
                <h3>{job.title}</h3>
                <p><strong>Assessment Required:</strong> {job.assessment_required ? 'Yes' : 'No'}</p>
                {job.description && <p>{job.description}</p>}
                
                <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem' }}>
                  <button 
                    className="btn btn-primary" 
                    onClick={() => handleApply(job.id)}
                  >
                    Apply Now
                  </button>
                  <Link to={`/student/jobs/${job.id}`} className="btn btn-secondary">
                    View Details
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
