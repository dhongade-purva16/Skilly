import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import apiClient from '../../services/apiClient';

export const CompanyApplicants = () => {
  const { jobId } = useParams<{ jobId: string }>();
  const [applicants, setApplicants] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchApplicants = async () => {
      try {
        const response = await apiClient.get(`/company/jobs/${jobId}/applications`);
        setApplicants(response.data);
      } catch (err: any) {
        setError('Failed to load applicants.');
      } finally {
        setLoading(false);
      }
    };
    fetchApplicants();
  }, [jobId]);

  const handleShortlist = async (applicationId: number) => {
    try {
      await apiClient.post(`/company/applications/${applicationId}/shortlist`);
      setApplicants(applicants.map(app => app.id === applicationId ? { ...app, status: 'shortlisted' } : app));
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to shortlist candidate.');
    }
  };

  if (loading) return <div>Loading applicants...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="page-container">
      <h1>Job Applicants</h1>
      <div style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {applicants.length === 0 ? (
          <p>No applicants yet.</p>
        ) : (
          applicants.map(app => (
            <div key={app.id} className="card" style={{ padding: '1rem', border: '1px solid #ddd', borderRadius: '8px' }}>
              <h3>Student ID: {app.student_id}</h3>
              <p>Status: {app.status}</p>
              {app.assessment_score !== null && <p>Assessment Score: {app.assessment_score}%</p>}
              {app.status !== 'shortlisted' && (
                <button 
                  onClick={() => handleShortlist(app.id)}
                  className="btn btn-primary"
                  style={{ marginTop: '1rem' }}
                >
                  Shortlist
                </button>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
