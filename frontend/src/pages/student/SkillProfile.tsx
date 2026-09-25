import { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { getStudentSkills, type StudentSkill } from '../../services/skill';
import { Link } from 'react-router-dom';
import './SkillProfile.css';

export const SkillProfile = () => {
  const [skills, setSkills] = useState<StudentSkill[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSkills = async () => {
      try {
        setLoading(true);
        const data = await getStudentSkills();
        setSkills(data);
      } catch (err) {
        setError('Failed to load skill profile.');
      } finally {
        setLoading(false);
      }
    };
    fetchSkills();
  }, []);

  if (loading) {
    return <div className="page loading">Loading skill profile...</div>;
  }

  return (
    <div className="page skill-profile-page">
      <div className="page-header">
        <h2>Your Skill Profile</h2>
        <Link to="/student/assessments" className="btn-primary">Take Assessment</Link>
      </div>

      {error && <div className="alert error">{error}</div>}

      {skills.length === 0 && !error ? (
        <Card className="empty-state">
          <h3>No skills assessed yet</h3>
          <p>Complete a skill assessment to build your skill profile and track your progress.</p>
          <Link to="/student/assessments" className="btn-secondary mt-4 inline-block">
            View Available Assessments
          </Link>
        </Card>
      ) : (
        <div className="skills-grid">
          {skills.map((studentSkill) => (
            <Card key={studentSkill.id} className="skill-card">
              <div className="skill-header">
                <h3>{studentSkill.skill.name}</h3>
                <span className="skill-badge">Level {studentSkill.proficiency_level}</span>
              </div>
              <div className="skill-category">
                {studentSkill.skill.category?.name || 'Uncategorized'}
              </div>
              
              <div className="skill-progress">
                <div className="progress-bar-container">
                  <div 
                    className="progress-bar" 
                    style={{ width: `${studentSkill.score}%` }}
                  ></div>
                </div>
                <div className="progress-stats">
                  <span>Score: {studentSkill.score.toFixed(1)}%</span>
                  {studentSkill.last_assessed_at && (
                    <span className="last-assessed">
                      Last Assessed: {new Date(studentSkill.last_assessed_at).toLocaleDateString()}
                    </span>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
