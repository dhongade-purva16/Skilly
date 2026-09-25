import { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { useAuth } from '../../contexts/AuthContext';
import { getStudentProfile, getAcademicProfile, getCareerGoal } from '../../services/student';
import { getStudentSkills, getStudentSkillGaps } from '../../services/skill';
import { getAssessments } from '../../services/assessment';
import { Link } from 'react-router-dom';
import './Dashboard.css';

export const StudentDashboard = () => {
  const { currentUser: user } = useAuth();
  
  const [loading, setLoading] = useState(true);
  
  const [profileComplete, setProfileComplete] = useState(false);
  const [careerRoleName, setCareerRoleName] = useState<string | null>(null);
  
  const [assessedSkillsCount, setAssessedSkillsCount] = useState(0);
  const [availableAssessments, setAvailableAssessments] = useState(0);
  
  const [gapsToClose, setGapsToClose] = useState(0);
  
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const [profile, academic, goal, skills, gaps, assessments] = await Promise.all([
          getStudentProfile().catch(() => null),
          getAcademicProfile().catch(() => null),
          getCareerGoal().catch(() => null),
          getStudentSkills().catch(() => []),
          getStudentSkillGaps().catch(() => []),
          getAssessments().catch(() => [])
        ]);
        
        // Basic profile completion logic
        let complete = true;
        if (!profile || !profile.full_name || !profile.phone) complete = false;
        if (!academic || !academic.degree || !academic.academic_year) complete = false;
        setProfileComplete(complete);
        
        if (goal && goal.career_role) {
          setCareerRoleName(goal.career_role.name);
        }
        
        setAssessedSkillsCount(skills.length);
        setAvailableAssessments(assessments.length);
        
        const missingOrGap = gaps.filter(g => g.gap_status !== 'Sufficient');
        setGapsToClose(missingOrGap.length);
        
      } catch (err) {
        console.error('Dashboard error:', err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchDashboardData();
  }, []);

  if (loading) {
    return <div className="page loading">Loading dashboard...</div>;
  }

  return (
    <div className="page dashboard-page">
      <div className="dashboard-header">
        <h2>Welcome back, {user?.email}</h2>
        <p className="subtitle">Here is your Phase 1 Student Intelligence overview.</p>
      </div>

      <div className="dashboard-grid">
        <Card className="dashboard-card">
          <h3>Profile Status</h3>
          <div className="status-display">
            <span className={`status-icon ${profileComplete ? 'complete' : 'incomplete'}`}>
              {profileComplete ? '✓' : '!'}
            </span>
            <span className="status-text">
              {profileComplete ? 'Profile Complete' : 'Profile Incomplete'}
            </span>
          </div>
          {!profileComplete && (
            <Link to="/student/profile" className="btn-secondary sm mt-3 block text-center">Complete Profile</Link>
          )}
        </Card>

        <Card className="dashboard-card">
          <h3>Career Goal</h3>
          <div className="role-display">
            {careerRoleName ? (
              <span className="role-name">{careerRoleName}</span>
            ) : (
              <span className="text-muted">No target role selected</span>
            )}
          </div>
          <Link to="/student/profile" className="btn-secondary sm mt-3 block text-center">Update Goal</Link>
        </Card>

        <Card className="dashboard-card">
          <h3>Skill Summary</h3>
          <div className="stat-big">{assessedSkillsCount}</div>
          <p className="stat-desc">Assessed Skills</p>
          <Link to="/student/skills" className="btn-secondary sm mt-3 block text-center">View Profile</Link>
        </Card>

        <Card className="dashboard-card">
          <h3>Skill Gaps</h3>
          <div className="stat-big">{gapsToClose}</div>
          <p className="stat-desc">Gaps to Close for Target Role</p>
          <Link to="/student/skill-gaps" className="btn-secondary sm mt-3 block text-center">Analyze Gaps</Link>
        </Card>

        <Card className="dashboard-card">
          <h3>Assessments</h3>
          <div className="stat-big">{availableAssessments}</div>
          <p className="stat-desc">Available Assessments</p>
          <Link to="/student/assessments" className="btn-secondary sm mt-3 block text-center">Take Assessment</Link>
        </Card>
      </div>
    </div>
  );
};