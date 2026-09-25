import { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { getAssessments, type Assessment } from '../../services/assessment';
import { useNavigate } from 'react-router-dom';
import './Assessments.css';

export const Assessments = () => {
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAssessments = async () => {
      try {
        setLoading(true);
        const data = await getAssessments();
        setAssessments(data);
      } catch (err) {
        setError('Failed to load assessments.');
      } finally {
        setLoading(false);
      }
    };
    fetchAssessments();
  }, []);

  if (loading) {
    return <div className="page loading">Loading assessments...</div>;
  }

  return (
    <div className="page assessments-page">
      <div className="page-header">
        <h2>Available Skill Assessments</h2>
        <p className="subtitle">Take validated skill assessments to prove your capabilities.</p>
      </div>

      {error && <div className="alert error">{error}</div>}

      {assessments.length === 0 && !error ? (
        <Card className="empty-state">
          <h3>No Assessments Available</h3>
          <p>There are currently no skill assessments available. Please check back later.</p>
        </Card>
      ) : (
        <div className="assessments-grid">
          {assessments.map((assessment) => (
            <Card key={assessment.id} className="assessment-card">
              <div className="assessment-content">
                <div style={{ display: 'flex', gap: '8px', marginBottom: '8px', flexWrap: 'wrap' }}>
                  <span className="skill-tag">{assessment.skill?.name}</span>
                  {assessment.assessment_source === 'company_specific' ? (
                    <span className="source-tag company-specific" style={{ fontSize: '0.75rem', padding: '2px 8px' }}>
                      Company Specific ({assessment.target_company_name || 'Target Company'})
                    </span>
                  ) : (
                    <span className="source-tag role-fallback" style={{ fontSize: '0.75rem', padding: '2px 8px' }}>
                      Role Fallback Assessment
                    </span>
                  )}
                </div>
                <h3>{assessment.title}</h3>
                <p>{assessment.description || 'Test your knowledge on this skill.'}</p>
              </div>
              <div className="assessment-actions" style={{ marginTop: '16px' }}>
                <button 
                  className="btn-primary"
                  onClick={() => navigate(`/student/assessments/${assessment.id}`)}
                >
                  Take Assessment
                </button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
