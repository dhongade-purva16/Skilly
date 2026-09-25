import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '../../services/apiClient';

export const CompanyAssessmentBuilder = () => {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    total_marks: 100,
    passing_criteria: 50.0,
    questions: [
      {
        question_text: '',
        options: ['', '', '', ''],
        correct_option_index: 0,
        skill_id: 1, // Placeholder skill_id
      },
    ],
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await apiClient.post(`/company/jobs/${jobId}/assessment`, formData);
      navigate(`/company/jobs/${jobId}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create assessment.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <h1>Assessment Builder</h1>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', maxWidth: '800px' }}>
        <div>
          <label>Title</label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            required
            className="input-field"
            style={{ width: '100%' }}
          />
        </div>
        
        {/* Further inputs for total marks and questions omitted for brevity in minimal implementation */}
        <p>A basic assessment form is initialized. Edit code to add full options matrix.</p>

        <button type="submit" disabled={loading} className="btn btn-primary">
          {loading ? 'Saving...' : 'Save Assessment'}
        </button>
      </form>
    </div>
  );
};
