import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import apiClient from '../../services/apiClient';

export const StudentApplications = () => {
  const [apps, setApps] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchApps = async () => {
      try {
        const response = await apiClient.get('/student/applications');
        setApps(response.data);
      } catch (error) {
        console.error('Failed to fetch applications', error);
      } finally {
        setLoading(false);
      }
    };
    fetchApps();
  }, []);

  if (loading) return <div>Loading applications...</div>;

  return (
    <div className="page-container">
      <header className="page-header">
        <h1>My Applications</h1>
        <p>Track your job and internship applications</p>
      </header>

      <div className="content-section" style={{ padding: '2rem' }}>
        {apps.length === 0 ? (
          <p>You haven't applied to any jobs yet.</p>
        ) : (
          <div className="apps-list" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {apps.map(app => (
              <div key={app.id} className="card" style={{ padding: '1.5rem', border: '1px solid #ccc', borderRadius: '8px' }}>
                <h3>Application #{app.id} (Job ID: {app.job_id})</h3>
                <p><strong>Status:</strong> <span style={{ textTransform: 'capitalize' }}>{app.status.replace('_', ' ')}</span></p>
                <p><strong>Applied At:</strong> {new Date(app.applied_at).toLocaleDateString()}</p>
                
                {app.status === 'assessment_pending' && (
                  <div style={{ marginTop: '1rem' }}>
                    <Link to={`/student/assessments/${app.id}`} className="btn btn-primary">Take Assessment</Link>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
