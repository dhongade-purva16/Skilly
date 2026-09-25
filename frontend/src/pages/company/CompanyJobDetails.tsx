import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import apiClient from '../../services/apiClient';

export const CompanyJobDetails = () => {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();
  const [job, setJob] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchJob = async () => {
      try {
        const response = await apiClient.get(`/company/jobs/${jobId}`);
        setJob(response.data);
      } catch (err: any) {
        setError('Failed to load job details.');
      } finally {
        setLoading(false);
      }
    };
    fetchJob();
  }, [jobId]);

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this job?')) {
      try {
        await apiClient.delete(`/company/jobs/${jobId}`);
        navigate('/company/jobs');
      } catch (err) {
        alert('Failed to delete job.');
      }
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;
  if (!job) return <div>Job not found.</div>;

  return (
    <div className="page-container">
      <h1>{job.title}</h1>
      <div className="card" style={{ padding: '1.5rem', marginTop: '1rem' }}>
        <p><strong>Description:</strong> {job.description}</p>
        <p><strong>Status:</strong> {job.status}</p>
        <p><strong>Assessment Required:</strong> {job.assessment_required ? 'Yes' : 'No'}</p>
        
        <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
          <Link to={`/company/jobs/${job.id}/applicants`} className="btn btn-primary">View Applicants</Link>
          <button onClick={handleDelete} className="btn btn-secondary" style={{ backgroundColor: 'red', color: 'white' }}>Delete Job</button>
        </div>
      </div>
    </div>
  );
};
