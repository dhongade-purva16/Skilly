import { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { 
  getStudentProfile, updateStudentProfile,
  getAcademicProfile, updateAcademicProfile,
  getCareerGoal, updateCareerGoal, getCareerRoles, getTargetCompanies,
  type StudentProfile, type AcademicProfile, type CareerRole, type TargetCompany
} from '../../services/student';
import { useNavigate } from 'react-router-dom';
import './Onboarding.css';

export const Onboarding = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [roles, setRoles] = useState<CareerRole[]>([]);
  const [companies, setCompanies] = useState<TargetCompany[]>([]);

  const [personal, setPersonal] = useState<StudentProfile>({});
  const [academic, setAcademic] = useState<AcademicProfile>({});
  const [careerGoalId, setCareerGoalId] = useState<number | ''>('');
  const [targetCompanyId, setTargetCompanyId] = useState<number | ''>('');

  useEffect(() => {
    const init = async () => {
      try {
        setLoading(true);
        const [profile, acad, goal, r, comp] = await Promise.all([
          getStudentProfile().catch(() => ({})),
          getAcademicProfile().catch(() => ({})),
          getCareerGoal().catch(() => ({ career_role_id: '', target_company_id: '' })),
          getCareerRoles().catch(() => []),
          getTargetCompanies().catch(() => [])
        ]);

        const isComplete = profile?.full_name && acad?.degree && goal?.career_role_id;
        if (isComplete) {
          navigate('/student/dashboard', { replace: true });
          return;
        }

        setPersonal(profile || {});
        setAcademic(acad || {});
        setCareerGoalId((goal?.career_role_id as any) || '');
        setTargetCompanyId((goal?.target_company_id as any) || '');
        setRoles(r);
        setCompanies(comp);
      } catch (err) {
        setError('Failed to load data');
      } finally {
        setLoading(false);
      }
    };
    init();
  }, [navigate]);

  const handleNext = async () => {
    try {
      setSaving(true);
      setError(null);
      if (step === 1) {
        await updateStudentProfile(personal);
        setStep(2);
      } else if (step === 2) {
        await updateAcademicProfile(academic);
        setStep(3);
      } else if (step === 3) {
        if (careerGoalId !== '') {
          await updateCareerGoal(Number(careerGoalId), targetCompanyId !== '' ? Number(targetCompanyId) : null);
        }
        navigate('/student/dashboard', { replace: true });
      }
    } catch (err) {
      setError('Failed to save. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="page loading">Loading...</div>;

  return (
    <div className="onboarding-page">
      <div className="onboarding-container">
        <h2>Welcome to SKILLY</h2>
        <p className="subtitle">Let's set up your profile to get started.</p>
        
        <div className="steps-indicator">
          <div className={`step-dot ${step >= 1 ? 'active' : ''}`}></div>
          <div className={`step-dot ${step >= 2 ? 'active' : ''}`}></div>
          <div className={`step-dot ${step >= 3 ? 'active' : ''}`}></div>
        </div>

        {error && <div className="alert error">{error}</div>}

        <Card className="onboarding-card">
          {step === 1 && (
            <div className="step-content">
              <h3>Step 1: Personal Information</h3>
              <div className="form-group">
                <label>Full Name</label>
                <input 
                  type="text" 
                  value={personal.full_name || ''} 
                  onChange={(e) => setPersonal({...personal, full_name: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Phone</label>
                <input 
                  type="tel" 
                  value={personal.phone || ''} 
                  onChange={(e) => setPersonal({...personal, phone: e.target.value})}
                />
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="step-content">
              <h3>Step 2: Academic Information</h3>
              <div className="form-group">
                <label>Degree</label>
                <input 
                  type="text" 
                  value={academic.degree || ''} 
                  onChange={(e) => setAcademic({...academic, degree: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Academic Year</label>
                <input 
                  type="text" 
                  value={academic.academic_year || ''} 
                  onChange={(e) => setAcademic({...academic, academic_year: e.target.value})}
                  placeholder="e.g. 3rd Year"
                />
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="step-content">
              <h3>Step 3: Target Career Objective</h3>
              <div className="form-group">
                <label>Select Target Role</label>
                <select 
                  value={careerGoalId} 
                  onChange={(e) => setCareerGoalId(e.target.value ? Number(e.target.value) : '')}
                >
                  <option value="" disabled>Select a role...</option>
                  {roles.map(r => (
                    <option key={r.id} value={r.id}>{r.name}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Target Company (Optional)</label>
                <select 
                  value={targetCompanyId} 
                  onChange={(e) => setTargetCompanyId(e.target.value ? Number(e.target.value) : '')}
                >
                  <option value="">None (Standard Role Objective)</option>
                  {companies.map(c => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
              </div>
            </div>
          )}

          <div className="form-actions mt-4" style={{ justifyContent: 'space-between' }}>
            {step > 1 ? (
              <button className="btn-secondary" onClick={() => setStep(step - 1)} disabled={saving}>Back</button>
            ) : (
              <div></div>
            )}
            
            <button className="btn-primary" onClick={handleNext} disabled={saving}>
              {saving ? 'Saving...' : (step === 3 ? 'Complete Setup' : 'Next')}
            </button>
          </div>
        </Card>
      </div>
    </div>
  );
};
