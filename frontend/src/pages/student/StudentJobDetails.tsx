import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '../../services/apiClient';

export const StudentJobDetails = () => {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();
  const [job, setJob] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [applying, setApplying] = useState(false);

  useEffect(() => {
    const fetchJob = async () => {
      try {
        const response = await apiClient.get(`/student/jobs/${jobId}`);
        setJob(response.data);
      } catch (err: any) {
        setError('Failed to load job details.');
      } finally {
        setLoading(false);
      }
    };
    fetchJob();
  }, [jobId]);

  const handleApply = async () => {
    setApplying(true);
    try {
      await apiClient.post(`/student/jobs/${jobId}/apply`);
      alert('Successfully applied!');
      navigate('/student/applications');
    } catch (err: any) {
      if (err.response?.status === 409) {
        alert('You have already applied to this job.');
      } else {
        alert('Failed to apply. Please try again later.');
      }
    } finally {
      setApplying(false);
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
        <p><strong>Assessment Required:</strong> {job.assessment_required ? 'Yes' : 'No'}</p>
        
        <div style={{ marginTop: '2rem' }}>
          <button onClick={handleApply} disabled={applying} className="btn btn-primary">
            {applying ? 'Applying...' : 'Apply Now'}
          </button>
        </div>
      </div>
    </div>
  );
};
