import { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { getStudentSkillGaps, type SkillGap } from '../../services/skill';
import { getCareerGoal, type CareerGoal } from '../../services/student';
import { Link } from 'react-router-dom';
import './SkillGaps.css';

export const SkillGaps = () => {
  const [gaps, setGaps] = useState<SkillGap[]>([]);
  const [goal, setGoal] = useState<CareerGoal | null>(null);
  const [hasGoal, setHasGoal] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchGaps = async () => {
      try {
        setLoading(true);
        const goalData = await getCareerGoal().catch(() => null);
        if (!goalData || !goalData.career_role_id) {
          setHasGoal(false);
          setLoading(false);
          return;
        }
        setGoal(goalData);
        setHasGoal(true);
        
        const data = await getStudentSkillGaps();
        setGaps(data);
      } catch (err) {
        setError('Failed to load skill gaps.');
      } finally {
        setLoading(false);
      }
    };
    fetchGaps();
  }, []);

  if (loading) {
    return <div className="page loading">Analyzing skill gaps...</div>;
  }

  if (hasGoal === false) {
    return (
      <div className="page skill-gaps-page">
        <div className="page-header">
          <h2>Skill Gap Analysis</h2>
        </div>
        <Card className="empty-state">
          <h3>No Target Role Selected</h3>
          <p>Select a target career role in your profile to analyze your skill gaps.</p>
          <Link to="/student/profile" className="btn-primary mt-4 inline-block">
            Update Profile
          </Link>
        </Card>
      </div>
    );
  }

  const missingOrGap = gaps.filter(g => g.gap_status !== 'Sufficient');
  const sufficient = gaps.filter(g => g.gap_status === 'Sufficient');

  const firstSource = gaps.length > 0 ? gaps[0].requirement_source : 'role_fallback';
  const companyName = gaps.length > 0 ? gaps[0].target_company_name : null;

  return (
    <div className="page skill-gaps-page">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2>Skill Gap Analysis</h2>
          {goal?.career_role && (
            <p className="subtitle">
              Targeting: <strong>{goal.career_role.name}</strong> 
              {goal.target_company && <span> at <strong>{goal.target_company.name}</strong></span>}
            </p>
          )}
        </div>

        {firstSource === 'company_specific' ? (
          <span className="source-tag company-specific">
            Company Specific ({companyName || 'Target Company'})
          </span>
        ) : (
          <span className="source-tag role-fallback">
            Role Fallback (Company requirements unavailable)
          </span>
        )}
      </div>

      {error && <div className="alert error">{error}</div>}

      <Card className="gaps-summary-card">
        <div className="summary-stats">
          <div className="stat-item">
            <span className="stat-value">{gaps.length}</span>
            <span className="stat-label">Required Skills</span>
          </div>
          <div className="stat-item">
            <span className="stat-value text-success">{sufficient.length}</span>
            <span className="stat-label">Sufficient</span>
          </div>
          <div className="stat-item">
            <span className="stat-value text-warning">{missingOrGap.length}</span>
            <span className="stat-label">Gaps to Close</span>
          </div>
        </div>
      </Card>

      {gaps.length === 0 ? (
        <Card className="empty-state mt-4">
          <h3>No Skills Required</h3>
          <p>The selected role does not have defined required skills yet.</p>
        </Card>
      ) : (
        <>
          <div className="gaps-section mt-4">
            <h3 className="section-title">Technical Skill Gaps</h3>
            <div className="gaps-table-container mt-2">
              <table className="gaps-table">
                <thead>
                  <tr>
                    <th>Skill</th>
                    <th>Category</th>
                    <th>Required Level</th>
                    <th>Current Level</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {gaps.filter(g => g.skill.category?.name !== 'Soft Skills').length === 0 && (
                    <tr>
                      <td colSpan={5} className="text-center text-muted">No technical skills required for this role.</td>
                    </tr>
                  )}
                  {gaps.filter(g => g.skill.category?.name !== 'Soft Skills').map((gap) => (
                    <tr key={gap.skill.id} className={`status-${gap.gap_status.toLowerCase()}`}>
                      <td className="font-medium">{gap.skill.name}</td>
                      <td className="text-muted">{gap.skill.category?.name || 'Uncategorized'}</td>
                      <td>Level {gap.required_level}</td>
                      <td>{gap.current_level > 0 ? `Level ${gap.current_level}` : 'Not Assessed'}</td>
                      <td>
                        <span className={`status-badge badge-${gap.gap_status.toLowerCase()}`}>
                          {gap.gap_status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="gaps-section mt-4">
            <h3 className="section-title">Soft Skill Gaps</h3>
            <div className="gaps-table-container mt-2">
              <table className="gaps-table">
                <thead>
                  <tr>
                    <th>Skill</th>
                    <th>Category</th>
                    <th>Required Level</th>
                    <th>Current Level</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {gaps.filter(g => g.skill.category?.name === 'Soft Skills').length === 0 && (
                    <tr>
                      <td colSpan={5} className="text-center text-muted">No soft skills required for this role.</td>
                    </tr>
                  )}
                  {gaps.filter(g => g.skill.category?.name === 'Soft Skills').map((gap) => (
                    <tr key={gap.skill.id} className={`status-${gap.gap_status.toLowerCase()}`}>
                      <td className="font-medium">{gap.skill.name}</td>
                      <td className="text-muted">{gap.skill.category?.name || 'Uncategorized'}</td>
                      <td>Level {gap.required_level}</td>
                      <td>{gap.current_level > 0 ? `Level ${gap.current_level}` : 'Not Assessed'}</td>
                      <td>
                        <span className={`status-badge badge-${gap.gap_status.toLowerCase()}`}>
                          {gap.gap_status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
