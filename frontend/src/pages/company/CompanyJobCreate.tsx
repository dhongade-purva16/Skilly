import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../../services/apiClient';

export const CompanyJobCreate = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    assessment_required: false,
    skills: [] as { skill_id: number; required_level: number; priority: string }[],
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await apiClient.post('/company/jobs', formData);
      navigate('/company/jobs');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create job');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <h1>Create New Job</h1>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', maxWidth: '600px' }}>
        <div>
          <label>Job Title</label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            required
            className="input-field"
            style={{ width: '100%' }}
          />
        </div>
        <div>
          <label>Description</label>
          <textarea
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="input-field"
            style={{ width: '100%', minHeight: '100px' }}
          />
        </div>
        <div>
          <label>
            <input
              type="checkbox"
              checked={formData.assessment_required}
              onChange={(e) => setFormData({ ...formData, assessment_required: e.target.checked })}
            />
            Assessment Required
          </label>
        </div>
        {/* Placeholder for skill selection - a real UI would fetch skills and let you add them */}
        <button type="button" onClick={() => setFormData({...formData, skills: [...formData.skills, { skill_id: 1, required_level: 3, priority: 'MEDIUM' }]})} className="btn btn-secondary">
          Add Mock Skill (ID: 1)
        </button>

        <button type="submit" disabled={loading} className="btn btn-primary">
          {loading ? 'Creating...' : 'Create Job'}
        </button>
      </form>
    </div>
  );
};
