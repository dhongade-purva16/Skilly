import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiClient from '../../services/apiClient';

export const StudentAssessmentView = () => {
  const { applicationId } = useParams<{ applicationId: string }>();
  const navigate = useNavigate();
  const [assessment, setAssessment] = useState<any>(null);
  const [attempt, setAttempt] = useState<any>(null);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    const fetchAssessment = async () => {
      try {
        const response = await apiClient.get(`/student/applications/${applicationId}/assessment`);
        setAssessment(response.data);
      } catch (err: any) {
        setError('Failed to load assessment.');
      } finally {
        setLoading(false);
      }
    };
    fetchAssessment();
  }, [applicationId]);

  const handleStart = async () => {
    try {
      const response = await apiClient.post(`/student/applications/${applicationId}/assessment/start`);
      setAttempt(response.data);
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to start assessment.');
    }
  };

  const handleSubmit = async () => {
    if (!attempt) return;
    setSubmitting(true);
    try {
      const response = await apiClient.post(`/student/assessments/${attempt.id}/submit`, { answers });
      setResult(response.data);
    } catch (err: any) {
      alert('Failed to submit assessment.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;
  if (!assessment) return <div>Assessment not found.</div>;

  if (result) {
    return (
      <div className="page-container">
        <h1>Assessment Completed</h1>
        <div className="card" style={{ padding: '1.5rem', marginTop: '1rem' }}>
          <h2>Overall Score: {result.overall_score}%</h2>
          <h3>Skill Performance:</h3>
          <ul>
            {Object.entries(result.skill_wise_scores).map(([skill, score]: any) => (
              <li key={skill}>{skill}: {score}%</li>
            ))}
          </ul>
          <button onClick={() => navigate('/student/applications')} className="btn btn-primary" style={{ marginTop: '1rem' }}>Back to Applications</button>
        </div>
      </div>
    );
  }

  if (!attempt) {
    return (
      <div className="page-container">
        <h1>{assessment.title}</h1>
        <p>Total Marks: {assessment.total_marks}</p>
        <p>Passing Criteria: {assessment.passing_criteria}%</p>
        <button onClick={handleStart} className="btn btn-primary" style={{ marginTop: '1rem' }}>Start Assessment</button>
      </div>
    );
  }

  return (
    <div className="page-container">
      <h1>{assessment.title}</h1>
      <div style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
        {assessment.questions.map((q: any) => (
          <div key={q.id} className="card" style={{ padding: '1.5rem', border: '1px solid #ddd', borderRadius: '8px' }}>
            <h3>{q.question_text}</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '1rem' }}>
              {q.options.map((opt: string, idx: number) => (
                <label key={idx} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <input
                    type="radio"
                    name={`q-${q.id}`}
                    value={idx}
                    checked={answers[q.id] === idx}
                    onChange={() => setAnswers({ ...answers, [q.id]: idx })}
                  />
                  {opt}
                </label>
              ))}
            </div>
          </div>
        ))}
      </div>
      <button 
        onClick={handleSubmit} 
        disabled={submitting} 
        className="btn btn-primary"
        style={{ marginTop: '2rem' }}
      >
        {submitting ? 'Submitting...' : 'Submit Assessment'}
      </button>
    </div>
  );
};
