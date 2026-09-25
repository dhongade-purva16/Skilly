import React, { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { 
  getStudentProfile, 
  updateStudentProfile, 
  getAcademicProfile, 
  updateAcademicProfile,
  getProfessionalProfile,
  updateProfessionalProfile,
  getExternalProfiles,
  updateExternalProfiles,
  syncGitHubProfile,
  uploadResume,
  getActiveResume,
  getResumeDownloadUrl,
  getStudentEvidence,
  getCareerGoal,
  updateCareerGoal,
  getCareerRoles,
  getTargetCompanies,
  getTargetCompanyRoles,
  type StudentProfile,
  type AcademicProfile,
  type ProfessionalProfile,
  type ExternalProfiles,
  type StudentResume,
  type StudentEvidence,
  type CareerRole,
  type TargetCompany
} from '../../services/student';
import { useAuth } from '../../contexts/AuthContext';
import './Profile.css';

export const Profile = () => {
  const { currentUser: user } = useAuth();
  
  const [loading, setLoading] = useState(true);
  const [globalError, setGlobalError] = useState<string | null>(null);

  // Section saving & status states
  const [savingPersonal, setSavingPersonal] = useState(false);
  const [personalMsg, setPersonalMsg] = useState<{ text: string; isError: boolean } | null>(null);

  const [savingAcademic, setSavingAcademic] = useState(false);
  const [academicMsg, setAcademicMsg] = useState<{ text: string; isError: boolean } | null>(null);

  const [savingProf, setSavingProf] = useState(false);
  const [profMsg, setProfMsg] = useState<{ text: string; isError: boolean } | null>(null);

  const [savingExternal, setSavingExternal] = useState(false);
  const [externalMsg, setExternalMsg] = useState<{ text: string; isError: boolean } | null>(null);

  const [savingGoal, setSavingGoal] = useState(false);
  const [goalMsg, setGoalMsg] = useState<{ text: string; isError: boolean } | null>(null);

  const [syncingGitHub, setSyncingGitHub] = useState(false);
  const [uploadingResume, setUploadingResume] = useState(false);
  const [resumeError, setResumeError] = useState<string | null>(null);
  const [resumeSuccess, setResumeSuccess] = useState<string | null>(null);

  // Data states
  const [allRoles, setAllRoles] = useState<CareerRole[]>([]);
  const [filteredRoles, setFilteredRoles] = useState<CareerRole[]>([]);
  const [companies, setCompanies] = useState<TargetCompany[]>([]);
  const [loadingCompanies, setLoadingCompanies] = useState(false);
  const [companyError, setCompanyError] = useState<string | null>(null);
  const [loadingRoles, setLoadingRoles] = useState(false);

  const [personal, setPersonal] = useState<StudentProfile>({
    full_name: '',
    phone: '',
    location: '',
    bio: ''
  });

  const [academic, setAcademic] = useState<AcademicProfile>({
    degree: '',
    branch: '',
    academic_year: '',
    graduation_year: undefined
  });

  const [professional, setProfessional] = useState<ProfessionalProfile>({
    headline: '',
    current_status: '',
    experience_level: '',
    years_of_experience: undefined,
    professional_summary: '',
    work_domain: ''
  });

  const [external, setExternal] = useState<ExternalProfiles>({
    github_url: '',
    linkedin_url: '',
    portfolio_url: '',
    linkedin_sync_status: 'Not Synced'
  });

  const [activeResume, setActiveResume] = useState<StudentResume | null>(null);
  const [evidenceList, setEvidenceList] = useState<StudentEvidence[]>([]);

  const [careerGoalId, setCareerGoalId] = useState<number | ''>('');
  const [targetCompanyId, setTargetCompanyId] = useState<number | ''>('');

  const fetchProfileData = async () => {
    try {
      setLoading(true);
      setGlobalError(null);
      setLoadingCompanies(true);
      
      const [
        profileData, 
        academicData, 
        profData, 
        extData, 
        resumeData, 
        evidenceData, 
        goalData, 
        rolesData, 
        compData
      ] = await Promise.all([
        getStudentProfile().catch(() => ({} as any)),
        getAcademicProfile().catch(() => ({} as any)),
        getProfessionalProfile().catch(() => ({} as any)),
        getExternalProfiles().catch(() => ({} as any)),
        getActiveResume().catch(() => null),
        getStudentEvidence().catch(() => []),
        getCareerGoal().catch(() => ({ career_role_id: '', target_company_id: '' } as any)),
        getCareerRoles().catch(() => []),
        getTargetCompanies().catch((_err: any) => {
          setCompanyError('Unable to load target companies. Please check your network.');
          return [];
        })
      ]);

      if (profileData) {
        setPersonal({
          full_name: profileData.full_name || '',
          phone: profileData.phone || '',
          location: profileData.location || '',
          bio: profileData.bio || ''
        });
      }
      
      if (academicData) {
        setAcademic({
          degree: academicData.degree || '',
          branch: academicData.branch || '',
          academic_year: academicData.academic_year || '',
          graduation_year: academicData.graduation_year || undefined
        });
      }

      if (profData) {
        setProfessional({
          headline: profData.headline || '',
          current_status: profData.current_status || 'Student',
          experience_level: profData.experience_level || 'Fresher',
          years_of_experience: profData.years_of_experience || 0,
          professional_summary: profData.professional_summary || '',
          work_domain: profData.work_domain || ''
        });
      }

      if (extData) {
        setExternal({
          github_url: extData.github_url || '',
          linkedin_url: extData.linkedin_url || '',
          portfolio_url: extData.portfolio_url || '',
          linkedin_sync_status: extData.linkedin_sync_status || 'Not Synced'
        });
      }

      setActiveResume(resumeData);
      setEvidenceList(evidenceData);
      setAllRoles(rolesData);
      setFilteredRoles(rolesData);
      setCompanies(compData);

      if (goalData) {
        const cId = (goalData.target_company_id as any) || '';
        const rId = (goalData.career_role_id as any) || '';
        setTargetCompanyId(cId);
        setCareerGoalId(rId);

        if (cId !== '') {
          fetchRolesForCompany(Number(cId), rolesData, rId);
        }
      }
    } catch (err) {
      setGlobalError('Failed to load profile data.');
    } finally {
      setLoading(false);
      setLoadingCompanies(false);
    }
  };

  const fetchRolesForCompany = async (companyId: number, baseRoles: CareerRole[], currentRoleId?: number | '') => {
    try {
      setLoadingRoles(true);
      const companyRoles = await getTargetCompanyRoles(companyId);
      if (companyRoles && companyRoles.length > 0) {
        const mappedRoles = companyRoles.map(cr => cr.career_role);
        setFilteredRoles(mappedRoles);
        // Clear role if current selected role is not available in new company's role list
        if (currentRoleId && !mappedRoles.some(r => r.id === currentRoleId)) {
          setCareerGoalId('');
        }
      } else {
        setFilteredRoles(baseRoles);
      }
    } catch (err) {
      setFilteredRoles(baseRoles);
    } finally {
      setLoadingRoles(false);
    }
  };

  useEffect(() => {
    fetchProfileData();
  }, []);

  const handleCompanyChange = (companyIdVal: string) => {
    if (companyIdVal === '') {
      setTargetCompanyId('');
      setFilteredRoles(allRoles);
    } else {
      const cId = Number(companyIdVal);
      setTargetCompanyId(cId);
      fetchRolesForCompany(cId, allRoles, careerGoalId);
    }
  };

  // --- Independent Section Save Handlers ---

  const handleSavePersonal = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSavingPersonal(true);
      setPersonalMsg(null);
      await updateStudentProfile(personal);
      setPersonalMsg({ text: 'Personal information saved!', isError: false });
      setTimeout(() => setPersonalMsg(null), 3000);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || 'Failed to save personal information.';
      setPersonalMsg({ text: msg, isError: true });
    } finally {
      setSavingPersonal(false);
    }
  };

  const handleSaveAcademic = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSavingAcademic(true);
      setAcademicMsg(null);
      await updateAcademicProfile(academic);
      setAcademicMsg({ text: 'Academic profile saved!', isError: false });
      setTimeout(() => setAcademicMsg(null), 3000);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || 'Failed to save academic profile.';
      setAcademicMsg({ text: msg, isError: true });
    } finally {
      setSavingAcademic(false);
    }
  };

  const handleSaveProfessional = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSavingProf(true);
      setProfMsg(null);
      await updateProfessionalProfile(professional);
      setProfMsg({ text: 'Professional profile saved!', isError: false });
      setTimeout(() => setProfMsg(null), 3000);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || 'Failed to save professional profile.';
      setProfMsg({ text: msg, isError: true });
    } finally {
      setSavingProf(false);
    }
  };

  const handleSaveExternal = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSavingExternal(true);
      setExternalMsg(null);
      await updateExternalProfiles(external);
      setExternalMsg({ text: 'External profiles saved!', isError: false });
      const freshEvidence = await getStudentEvidence().catch(() => []);
      setEvidenceList(freshEvidence);
      setTimeout(() => setExternalMsg(null), 3000);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || 'Failed to save external profiles.';
      setExternalMsg({ text: msg, isError: true });
    } finally {
      setSavingExternal(false);
    }
  };

  const handleSaveCareerGoal = async (e: React.FormEvent) => {
    e.preventDefault();
    if (careerGoalId === '') {
      setGoalMsg({ text: 'Please select a target job role.', isError: true });
      return;
    }
    try {
      setSavingGoal(true);
      setGoalMsg(null);
      await updateCareerGoal(Number(careerGoalId), targetCompanyId !== '' ? Number(targetCompanyId) : null);
      setGoalMsg({ text: 'Target career objective saved!', isError: false });
      setTimeout(() => setGoalMsg(null), 3000);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || 'Failed to save career goal.';
      setGoalMsg({ text: msg, isError: true });
    } finally {
      setSavingGoal(false);
    }
  };

  const handleGitHubSync = async () => {
    if (!external.github_url) {
      setExternalMsg({ text: 'Please enter and save your GitHub Profile URL first.', isError: true });
      return;
    }
    try {
      setSyncingGitHub(true);
      setExternalMsg(null);
      await syncGitHubProfile();
      setExternalMsg({ text: 'GitHub repositories synced as unverified evidence!', isError: false });
      const freshEvidence = await getStudentEvidence().catch(() => []);
      setEvidenceList(freshEvidence);
      setTimeout(() => setExternalMsg(null), 4000);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || 'Failed to sync GitHub profile.';
      setExternalMsg({ text: msg, isError: true });
    } finally {
      setSyncingGitHub(false);
    }
  };

  const handleResumeFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      setUploadingResume(true);
      setResumeError(null);
      setResumeSuccess(null);
      const res = await uploadResume(file);
      setActiveResume(res);
      setResumeSuccess(`Resume "${res.filename}" uploaded securely and text extracted!`);
      const freshEvidence = await getStudentEvidence().catch(() => []);
      setEvidenceList(freshEvidence);
      setTimeout(() => setResumeSuccess(null), 5000);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Resume upload failed.';
      setResumeError(msg);
    } finally {
      setUploadingResume(false);
    }
  };

  if (loading) {
    return <div className="page loading">Loading student profile...</div>;
  }

  return (
    <div className="page profile-page">
      <h2>Student Profile & Evidence Hub</h2>
      
      {globalError && <div className="alert error">{globalError}</div>}
      
      <div className="profile-grid">
        
        {/* Personal Information */}
        <Card className="profile-card">
          <form onSubmit={handleSavePersonal}>
            <h3>Personal Information</h3>
            {personalMsg && (
              <div className={`alert ${personalMsg.isError ? 'error' : 'success'}`}>
                {personalMsg.text}
              </div>
            )}
            
            <div className="form-group">
              <label>Email Address</label>
              <input type="email" value={user?.email || ''} disabled className="disabled-input" />
            </div>
            
            <div className="form-group">
              <label>Full Name</label>
              <input 
                type="text" 
                value={personal.full_name} 
                onChange={(e) => setPersonal({...personal, full_name: e.target.value})}
                placeholder="Enter your full name"
              />
            </div>
            
            <div className="form-group">
              <label>Phone Number</label>
              <input 
                type="tel" 
                value={personal.phone} 
                onChange={(e) => setPersonal({...personal, phone: e.target.value})}
                placeholder="Enter your phone number"
              />
            </div>

            <div className="form-group">
              <label>Location</label>
              <input 
                type="text" 
                value={personal.location} 
                onChange={(e) => setPersonal({...personal, location: e.target.value})}
                placeholder="City, Country"
              />
            </div>

            <div className="form-group">
              <label>Bio</label>
              <textarea 
                value={personal.bio} 
                onChange={(e) => setPersonal({...personal, bio: e.target.value})}
                placeholder="Tell us a bit about yourself"
                rows={3}
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="btn-primary" disabled={savingPersonal}>
                {savingPersonal ? 'Saving Personal...' : 'Save Personal Info'}
              </button>
            </div>
          </form>
        </Card>

        {/* Academic Information */}
        <Card className="profile-card">
          <form onSubmit={handleSaveAcademic}>
            <h3>Academic Information</h3>
            {academicMsg && (
              <div className={`alert ${academicMsg.isError ? 'error' : 'success'}`}>
                {academicMsg.text}
              </div>
            )}

            <div className="form-group">
              <label>Degree</label>
              <input 
                type="text" 
                value={academic.degree} 
                onChange={(e) => setAcademic({...academic, degree: e.target.value})}
                placeholder="e.g. Bachelor of Technology"
              />
            </div>

            <div className="form-group">
              <label>Branch / Specialization</label>
              <input 
                type="text" 
                value={academic.branch} 
                onChange={(e) => setAcademic({...academic, branch: e.target.value})}
                placeholder="e.g. Computer Science"
              />
            </div>

            <div className="form-group">
              <label>Academic Year</label>
              <input 
                type="text" 
                value={academic.academic_year} 
                onChange={(e) => setAcademic({...academic, academic_year: e.target.value})}
                placeholder="e.g. 3rd Year"
              />
            </div>

            <div className="form-group">
              <label>Graduation Year</label>
              <input 
                type="number" 
                value={academic.graduation_year || ''} 
                onChange={(e) => setAcademic({...academic, graduation_year: parseInt(e.target.value) || undefined})}
                placeholder="e.g. 2025"
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="btn-primary" disabled={savingAcademic}>
                {savingAcademic ? 'Saving Academic...' : 'Save Academic Info'}
              </button>
            </div>
          </form>
        </Card>

        {/* Professional Profile */}
        <Card className="profile-card">
          <form onSubmit={handleSaveProfessional}>
            <h3>Professional Profile</h3>
            {profMsg && (
              <div className={`alert ${profMsg.isError ? 'error' : 'success'}`}>
                {profMsg.text}
              </div>
            )}

            <div className="form-group">
              <label>Headline</label>
              <input 
                type="text" 
                value={professional.headline} 
                onChange={(e) => setProfessional({...professional, headline: e.target.value})}
                placeholder="e.g. Aspiring Backend Developer | Python Enthusiast"
              />
            </div>

            <div className="form-group">
              <label>Current Status</label>
              <input 
                type="text" 
                value={professional.current_status} 
                onChange={(e) => setProfessional({...professional, current_status: e.target.value})}
                placeholder="e.g. Student, Intern, Fresher"
              />
            </div>

            <div className="form-group">
              <label>Experience Level</label>
              <input 
                type="text" 
                value={professional.experience_level} 
                onChange={(e) => setProfessional({...professional, experience_level: e.target.value})}
                placeholder="e.g. Beginner, Intermediate, Fresher"
              />
            </div>

            <div className="form-group">
              <label>Years of Experience</label>
              <input 
                type="number" 
                step="0.5"
                value={professional.years_of_experience ?? ''} 
                onChange={(e) => setProfessional({...professional, years_of_experience: parseFloat(e.target.value) || 0})}
                placeholder="e.g. 0.5"
              />
            </div>

            <div className="form-group">
              <label>Professional Summary</label>
              <textarea 
                value={professional.professional_summary} 
                onChange={(e) => setProfessional({...professional, professional_summary: e.target.value})}
                placeholder="Brief summary of your professional background"
                rows={2}
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="btn-primary" disabled={savingProf}>
                {savingProf ? 'Saving Professional...' : 'Save Professional Info'}
              </button>
            </div>
          </form>
        </Card>

        {/* External Profiles */}
        <Card className="profile-card">
          <form onSubmit={handleSaveExternal}>
            <h3>External Profiles</h3>
            {externalMsg && (
              <div className={`alert ${externalMsg.isError ? 'error' : 'success'}`}>
                {externalMsg.text}
              </div>
            )}

            <div className="form-group">
              <label>GitHub Profile URL</label>
              <input 
                type="url" 
                value={external.github_url} 
                onChange={(e) => setExternal({...external, github_url: e.target.value})}
                placeholder="https://github.com/username"
              />
              <button 
                type="button" 
                className="btn-secondary btn-sm"
                onClick={handleGitHubSync}
                disabled={syncingGitHub || !external.github_url}
                style={{ marginTop: '6px' }}
              >
                {syncingGitHub ? 'Syncing Repos...' : 'Sync GitHub Repositories'}
              </button>
            </div>

            <div className="form-group">
              <label>LinkedIn Profile URL</label>
              <input 
                type="url" 
                value={external.linkedin_url} 
                onChange={(e) => setExternal({...external, linkedin_url: e.target.value})}
                placeholder="https://linkedin.com/in/username"
              />
              <div className="badge-sync-status" style={{ marginTop: '4px' }}>
                Status: <span className="status-tag not-synced">Not Synced</span>
                <small style={{ display: 'block', color: '#888' }}>OAuth integration unavailable</small>
              </div>
            </div>

            <div className="form-group">
              <label>Portfolio URL</label>
              <input 
                type="url" 
                value={external.portfolio_url} 
                onChange={(e) => setExternal({...external, portfolio_url: e.target.value})}
                placeholder="https://yourportfolio.com"
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="btn-primary" disabled={savingExternal}>
                {savingExternal ? 'Saving External...' : 'Save External Links'}
              </button>
            </div>
          </form>
        </Card>

        {/* Target Career Objective (Company & Job Role) */}
        <Card className="profile-card full-width">
          <form onSubmit={handleSaveCareerGoal}>
            <h3>Target Career Objective</h3>
            {goalMsg && (
              <div className={`alert ${goalMsg.isError ? 'error' : 'success'}`}>
                {goalMsg.text}
              </div>
            )}

            <div className="form-group">
              <label>Target Company (Optional)</label>
              {loadingCompanies ? (
                <p className="text-muted">Loading target companies...</p>
              ) : companyError ? (
                <div className="alert error">{companyError}</div>
              ) : companies.length === 0 ? (
                <p className="text-muted">No target companies available.</p>
              ) : (
                <select 
                  value={targetCompanyId} 
                  onChange={(e) => handleCompanyChange(e.target.value)}
                >
                  <option value="">None (Standard Role Objective)</option>
                  {companies.map(comp => (
                    <option key={comp.id} value={comp.id}>
                      {comp.name}
                    </option>
                  ))}
                </select>
              )}
              <small>Selecting a company will filter company-specific job roles & assessments.</small>
            </div>

            <div className="form-group">
              <label>Target Job Role</label>
              {loadingRoles ? (
                <p className="text-muted">Loading job roles for selected company...</p>
              ) : filteredRoles.length === 0 ? (
                <p className="text-muted">No target job roles available for this selection.</p>
              ) : (
                <select 
                  value={careerGoalId} 
                  onChange={(e) => setCareerGoalId(e.target.value === '' ? '' : Number(e.target.value))}
                  required
                >
                  <option value="" disabled>Select a career role...</option>
                  {filteredRoles.map(role => (
                    <option key={role.id} value={role.id}>
                      {role.name}
                    </option>
                  ))}
                </select>
              )}
              <small>Select your target career role.</small>
            </div>

            <div className="form-actions">
              <button type="submit" className="btn-primary" disabled={savingGoal}>
                {savingGoal ? 'Saving Career Objective...' : 'Save Career Objective'}
              </button>
            </div>
          </form>
        </Card>

        {/* Resume Management */}
        <Card className="profile-card full-width">
          <h3>Resume Document Storage</h3>
          <p className="section-desc">
            Upload your resume (PDF, DOC, DOCX, TXT). Saved to private backend storage with automatic server-side text extraction.
          </p>

          {resumeError && <div className="alert error">{resumeError}</div>}
          {resumeSuccess && <div className="alert success">{resumeSuccess}</div>}
          
          <div className="resume-upload-section">
            <input 
              type="file" 
              accept=".pdf,.docx,.doc,.txt"
              onChange={handleResumeFileUpload}
              disabled={uploadingResume}
              id="resume-file-input"
            />
            {uploadingResume && <span> Uploading & extracting text...</span>}
          </div>

          {activeResume && (
            <div className="active-resume-box" style={{ marginTop: '12px', padding: '12px', background: '#f8f9fa', borderRadius: '6px' }}>
              <strong>Current Active Resume:</strong> {activeResume.filename} ({(activeResume.file_size / 1024).toFixed(1)} KB)
              <br />
              <small>Uploaded at: {new Date(activeResume.uploaded_at).toLocaleString()}</small>
              <div style={{ marginTop: '6px' }}>
                <a 
                  href={getResumeDownloadUrl(activeResume.id)} 
                  target="_blank" 
                  rel="noreferrer"
                  className="btn-link"
                >
                  Download Secure Resume
                </a>
              </div>
            </div>
          )}
        </Card>

        {/* Generic Evidence Log */}
        <Card className="profile-card full-width">
          <h3>Generic Student Evidence Layer</h3>
          <p className="section-desc">
            All logged evidence (Resumes, GitHub repos, LinkedIn, Portfolio, Assessments). Note: Evidence remains unverified until formally assessed.
          </p>

          {evidenceList.length === 0 ? (
            <p>No evidence items logged yet.</p>
          ) : (
            <div className="evidence-table-container">
              <table className="evidence-table">
                <thead>
                  <tr>
                    <th>Source</th>
                    <th>Evidence Type</th>
                    <th>Details</th>
                    <th>Status</th>
                    <th>Created / Synced</th>
                  </tr>
                </thead>
                <tbody>
                  {evidenceList.map((ev) => (
                    <tr key={ev.id}>
                      <td><span className={`source-badge ${ev.source.toLowerCase()}`}>{ev.source}</span></td>
                      <td>{ev.evidence_type}</td>
                      <td>
                        {ev.source === 'GITHUB' && ev.extracted_data?.repo_count ? (
                          <span>Repos: {ev.extracted_data.repo_count} ({ev.extracted_data?.languages?.join(', ') || 'No langs'})</span>
                        ) : ev.source === 'RESUME' && ev.extracted_data?.filename ? (
                          <span>File: {ev.extracted_data.filename}</span>
                        ) : ev.source === 'LINKEDIN' ? (
                          <span>{ev.source_url}</span>
                        ) : ev.source === 'ASSESSMENT' && ev.extracted_data?.score !== undefined ? (
                          <span>Score: {ev.extracted_data.score}%</span>
                        ) : (
                          <span>{ev.source_url || 'N/A'}</span>
                        )}
                      </td>
                      <td>
                        <span className={`status-pill ${ev.verification_status}`}>
                          {ev.verification_status}
                        </span>
                      </td>
                      <td>{new Date(ev.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>

      </div>
    </div>
  );
};
