import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getAchieverContext, getAchieverPriorities, getAchieverResources, getRoadmap, generateRoadmap } from '../../services/achiever';
import type { AchieverContext, AchieverPriorityResponse, AchieverResourcesResponse, RoadmapResponse } from '../../services/achiever';
import { getStudentProfile, updateGemsPreferences, type StudentProfile } from '../../services/student';
import './AchieverContextPage.css';

const AchieverContextPage: React.FC = () => {
  const navigate = useNavigate();
  const [context, setContext] = useState<AchieverContext | null>(null);
  const [priorityData, setPriorityData] = useState<AchieverPriorityResponse | null>(null);
  const [resourcesData, setResourcesData] = useState<AchieverResourcesResponse | null>(null);
  const [roadmapData, setRoadmapData] = useState<RoadmapResponse | null>(null);
  const [studentProfile, setStudentProfile] = useState<StudentProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [generatingRoadmap, setGeneratingRoadmap] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchContext = async () => {
    try {
      setLoading(true);
      const [data, prioData, profile] = await Promise.all([
        getAchieverContext(),
        getAchieverPriorities(),
        getStudentProfile().catch(() => null)
      ]);
      setContext(data);
      setPriorityData(prioData);
      if (profile) setStudentProfile(profile);
      
      try {
        const resData = await getAchieverResources();
        setResourcesData(resData);
      } catch (resErr) {
        console.error('Failed to load Achiever Resources', resErr);
      }

      try {
        const rmData = await getRoadmap();
        setRoadmapData(rmData);
      } catch (rmErr) {
        console.error('Failed to load Roadmap', rmErr);
      }
      
      setError(null);
    } catch (err) {
      console.error('Failed to load Achiever Context', err);
      setError('Failed to load Achiever Context');
    } finally {
      setLoading(false);
    }
  };

  const handleEnableGems = async () => {
    try {
      await updateGemsPreferences({ gems_enabled: true });
      navigate('/student/gems');
    } catch (err) {
      console.error('Failed to enable GEMS', err);
      alert('Failed to enable GEMS.');
    }
  };

  const handleGenerateRoadmap = async () => {
    try {
      setGeneratingRoadmap(true);
      const newRoadmap = await generateRoadmap();
      setRoadmapData(newRoadmap);
    } catch (err) {
      console.error('Failed to generate roadmap', err);
      alert('Failed to generate roadmap. Please make sure you have a target role selected.');
    } finally {
      setGeneratingRoadmap(false);
    }
  };

  useEffect(() => {
    fetchContext();
  }, []);

  if (loading) return <div className="achiever-loading">Loading Achiever Context...</div>;
  if (error) return <div className="achiever-error">{error}</div>;
  if (!context) return null;

  return (
    <div className="achiever-page">
      <header className="achiever-header">
        <h1>ACHIEVER AI</h1>
        <p className="subtitle">Validation Interface for Context Engine</p>
      </header>

      <div className="achiever-grid">
        <section className="achiever-card">
          <h2>Target</h2>
          <div className="info-row">
            <span className="label">Target Company:</span>
            <span className="value">{context.target.target_company?.name || 'Not Selected'}</span>
          </div>
          <div className="info-row">
            <span className="label">Target Job Role:</span>
            <span className="value">{context.target.target_role?.name || context.target.career_role?.name || 'Not Selected'}</span>
          </div>
          <div className="info-row">
            <span className="label">Requirement Source:</span>
            <span className="value highlight">{context.metadata.requirement_source === 'company_specific' ? 'Company Specific' : (context.metadata.requirement_source === 'role_fallback' ? 'Role Fallback' : 'None')}</span>
          </div>
        </section>

        <section className="achiever-card">
          <h2>Profile</h2>
          <div className="info-row">
            <span className="label">Professional Headline:</span>
            <span className="value">{context.professional.headline || 'Not Available'}</span>
          </div>
          <div className="info-row">
            <span className="label">Current Position/Status:</span>
            <span className="value">{context.professional.current_status || 'Not Available'}</span>
          </div>
          <div className="info-row">
            <span className="label">Experience:</span>
            <span className="value">{context.professional.years_of_experience ? `${context.professional.years_of_experience} years` : 'Not Available'}</span>
          </div>
          <div className="info-row">
            <span className="label">Work Domain:</span>
            <span className="value">{context.professional.work_domain || 'Not Available'}</span>
          </div>
        </section>

        <section className="achiever-card">
          <h2>Evidence</h2>
          <div className="info-row">
            <span className="label">Resume:</span>
            <span className="value">{context.resume.active_status ? (context.resume.extraction_status === 'extracted' ? 'Uploaded & Analyzed [UNVERIFIED]' : 'Uploaded [UNVERIFIED]') : 'Not Uploaded'}</span>
          </div>
          <div className="info-row">
            <span className="label">GitHub:</span>
            <span className="value">{context.external_profiles.github_status === 'synced' ? 'Synced [UNVERIFIED]' : (context.external_profiles.github_status === 'url_only' ? 'URL Only [UNVERIFIED]' : 'Not Synced')}</span>
          </div>
          <div className="info-row">
            <span className="label">LinkedIn:</span>
            <span className="value">{context.external_profiles.linkedin_status === 'synced' ? 'Synced [UNVERIFIED]' : (context.external_profiles.linkedin_status === 'url_only' ? 'URL Only [UNVERIFIED]' : 'Not Synced')}</span>
          </div>
          <div className="info-row">
            <span className="label">Portfolio:</span>
            <span className="value">{context.external_profiles.portfolio_status === 'synced' ? 'Analyzed [UNVERIFIED]' : (context.external_profiles.portfolio_status === 'url_only' ? 'URL Only [UNVERIFIED]' : 'Not Provided')}</span>
          </div>
          <div className="info-row">
            <span className="label">Assessment:</span>
            <span className="value">{context.metadata.has_assessment ? 'Completed [VERIFIED]' : 'Not Taken'}</span>
          </div>
        </section>

        <section className="achiever-card full-width">
          <h2>Current Skills</h2>
          {context.skills.length > 0 ? (
            <table className="achiever-table">
              <thead>
                <tr>
                  <th>Skill</th>
                  <th>Current Proficiency</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {context.skills.map((s, idx) => (
                  <tr key={idx}>
                    <td>{s.skill.name}</td>
                    <td>{s.proficiency_level}/5</td>
                    <td>{s.source_status || 'Unknown'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="no-data">No skills recorded.</p>
          )}
        </section>

        <section className="achiever-card full-width">
          <h2>Skill Gaps</h2>
          {context.skill_gaps.length > 0 ? (
            <table className="achiever-table">
              <thead>
                <tr>
                  <th>Skill</th>
                  <th>Required</th>
                  <th>Current</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {context.skill_gaps.map((gap, idx) => (
                  <tr key={idx}>
                    <td>{gap.skill.name}</td>
                    <td>{gap.required_proficiency}/5</td>
                    <td>{gap.current_proficiency}/5</td>
                    <td>
                      <span className={`status-badge ${gap.status.toLowerCase()}`}>
                        {gap.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="no-data">No requirements or gaps calculated yet.</p>
          )}
        </section>

        <section className="achiever-card full-width">
          <h2>Skill Priority</h2>
          {!priorityData ? (
            <p className="no-data">Loading priorities...</p>
          ) : priorityData.prioritized_gaps.length > 0 ? (
            <table className="achiever-table">
              <thead>
                <tr>
                  <th>Skill</th>
                  <th>Current Level</th>
                  <th>Required Level</th>
                  <th>Gap Status</th>
                  <th>Priority</th>
                  <th>Requirement Source</th>
                  <th>Evidence</th>
                  <th>Reason</th>
                </tr>
              </thead>
              <tbody>
                {priorityData.prioritized_gaps.map((gap, idx) => (
                  <tr key={idx}>
                    <td>{gap.skill.name}</td>
                    <td>{gap.current_proficiency}/5</td>
                    <td>{gap.required_proficiency}/5</td>
                    <td><span className={`status-badge ${gap.gap_status.toLowerCase()}`}>{gap.gap_status}</span></td>
                    <td><strong>{gap.priority}</strong></td>
                    <td>{gap.requirement_source === 'company_specific' ? 'Company Specific' : (gap.requirement_source === 'role_fallback' ? 'Role Fallback' : gap.requirement_source)}</td>
                    <td>
                      {gap.evidence_summary.length > 0 ? (
                        <ul style={{ margin: 0, paddingLeft: '1rem' }}>
                          {gap.evidence_summary.map((ev, i) => (
                            <li key={i}>{ev.source}: {ev.status}</li>
                          ))}
                        </ul>
                      ) : (
                        'No evidence'
                      )}
                    </td>
                    <td>
                      <ul style={{ margin: 0, paddingLeft: '1rem' }}>
                        {gap.reasons.map((r, i) => (
                          <li key={i}>{r}</li>
                        ))}
                      </ul>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="no-data">{priorityData.summary}</p>
          )}
        </section>

        <section className="achiever-card full-width">
          <h2>Recommended Learning Resources</h2>
          {!resourcesData ? (
            <p className="no-data">Loading resources...</p>
          ) : resourcesData.resources.length > 0 ? (
            <table className="achiever-table">
              <thead>
                <tr>
                  <th>Skill</th>
                  <th>Priority</th>
                  <th>Resource Title</th>
                  <th>Resource Type</th>
                  <th>Provider</th>
                  <th>Difficulty</th>
                  <th>Duration</th>
                  <th>Status</th>
                  <th>Link</th>
                </tr>
              </thead>
              <tbody>
                {resourcesData.resources.map((group) => (
                  group.resources.map((res, i) => (
                    <tr key={`${group.skill_id}-${i}`}>
                      {i === 0 && (
                        <>
                          <td rowSpan={group.resources.length}>{group.skill_name}</td>
                          <td rowSpan={group.resources.length}><strong>{group.priority}</strong></td>
                        </>
                      )}
                      <td>{res.title}</td>
                      <td style={{textTransform: 'capitalize'}}>{res.resource_type}</td>
                      <td>{res.provider}</td>
                      <td style={{textTransform: 'capitalize'}}>{res.difficulty || 'Unknown'}</td>
                      <td>{res.estimated_duration || 'N/A'}</td>
                      <td><span className="status-badge verified">Trusted</span></td>
                      <td>
                        <a href={res.source_url} target="_blank" rel="noreferrer" style={{color: '#2563eb'}}>View</a>
                      </td>
                    </tr>
                  ))
                ))}
              </tbody>
            </table>
          ) : (
            <p className="no-data">No trusted learning resources are available for the current skill gaps.</p>
          )}
        </section>

        <section className="achiever-card full-width">
          <h2>Personalized Roadmap</h2>
          
          <div style={{ marginBottom: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <p style={{ margin: 0 }}>
              Based on your target role, skill priorities, and evidence gaps.
            </p>
            <button 
              className="btn-primary" 
              onClick={handleGenerateRoadmap}
              disabled={generatingRoadmap}
            >
              {generatingRoadmap ? 'Generating...' : (roadmapData ? 'Regenerate Roadmap' : 'Generate My Roadmap')}
            </button>
          </div>

          {!roadmapData ? (
            <p className="no-data">No roadmap generated yet.</p>
          ) : (
            <div className="roadmap-container">
              <div style={{ marginBottom: '1rem', padding: '1rem', background: '#f8fafc', borderRadius: '4px', border: '1px solid #e2e8f0' }}>
                <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem' }}>{roadmapData.summary}</h3>
                <p style={{ margin: 0, color: '#64748b' }}>Target: {roadmapData.target.role} {roadmapData.target.company ? `@ ${roadmapData.target.company}` : ''}</p>
              </div>

              {roadmapData.steps.length === 0 ? (
                <p className="no-data">No actionable steps identified. You might have sufficient skills for this role!</p>
              ) : (
                <div className="roadmap-steps">
                  {roadmapData.steps.map((step) => (
                    <div key={step.id} className="roadmap-step" style={{ padding: '1.25rem', border: '1px solid #cbd5e1', borderRadius: '6px', marginBottom: '1rem', borderLeft: '4px solid #3b82f6' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                        <div>
                          <span style={{ display: 'inline-block', background: '#e0e7ff', color: '#3730a3', padding: '0.2rem 0.6rem', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold', marginRight: '0.5rem' }}>
                            STEP {step.step_order}
                          </span>
                          <span className={`status-badge ${step.priority.toLowerCase()}`} style={{ marginRight: '0.5rem' }}>
                            {step.priority} PRIORITY
                          </span>
                          <span style={{ fontSize: '0.9rem', color: '#64748b' }}>
                            Est: {step.estimated_duration || 'Unknown'}
                          </span>
                        </div>
                        <span className={`status-badge ${step.status.toLowerCase()}`}>
                          {step.status.replace('_', ' ')}
                        </span>
                      </div>
                      
                      <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.25rem', color: '#0f172a' }}>{step.skill_name}</h3>
                      <p style={{ margin: '0 0 1rem 0', color: '#334155' }}><strong>Objective:</strong> {step.objective}</p>
                      
                      {step.practice_task && (
                        <div style={{ background: '#f1f5f9', padding: '1rem', borderRadius: '4px', marginBottom: '1rem' }}>
                          <h4 style={{ margin: '0 0 0.5rem 0', color: '#0f172a', fontSize: '0.95rem' }}>Practice Task</h4>
                          <p style={{ margin: 0, color: '#334155', fontSize: '0.9rem' }}>{step.practice_task}</p>
                        </div>
                      )}

                      {step.resources.length > 0 && (
                        <div>
                          <h4 style={{ margin: '0 0 0.5rem 0', color: '#0f172a', fontSize: '0.95rem' }}>Learning Resources</h4>
                          <ul style={{ margin: 0, paddingLeft: '1.25rem', color: '#334155', fontSize: '0.9rem' }}>
                            {step.resources.map(r => (
                              <li key={r.resource_id} style={{ marginBottom: '0.25rem' }}>
                                <a href={r.source_url} target="_blank" rel="noreferrer" style={{ color: '#2563eb', textDecoration: 'none' }}>
                                  {r.title}
                                </a>
                                <span style={{ color: '#94a3b8', marginLeft: '0.5rem' }}>({r.provider} - {r.difficulty || 'All levels'})</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {roadmapData.steps.length > 0 && (
                <div style={{ marginTop: '2rem', padding: '1.5rem', background: '#eef2ff', borderRadius: '8px', border: '1px solid #c7d2fe', textAlign: 'center' }}>
                  <h3 style={{ margin: '0 0 1rem 0', color: '#3730a3' }}>Turn Your Roadmap Into Daily Action</h3>
                  <p style={{ marginBottom: '1rem', color: '#4338ca' }}>
                    Your personalized roadmap is ready. Would you like SKILLY to convert these roadmap steps into manageable daily tasks and reminders?
                  </p>
                  <ul style={{ listStyle: 'none', padding: 0, margin: '0 0 1.5rem 0', color: '#4f46e5', display: 'inline-block', textAlign: 'left' }}>
                    <li>✓ Daily task generation</li>
                    <li>✓ Daily reminders</li>
                    <li>✓ Learn → Practice → Review</li>
                    <li>✓ Progress tracking</li>
                  </ul>
                  <br />
                  {studentProfile?.gems_enabled ? (
                    <button 
                      className="btn-primary" 
                      onClick={() => navigate('/student/gems')}
                    >
                      Open GEMS
                    </button>
                  ) : (
                    <button 
                      className="btn-primary" 
                      onClick={handleEnableGems}
                    >
                      Enable GEMS
                    </button>
                  )}
                </div>
              )}
            </div>
          )}
        </section>
      </div>
    </div>
  );
};

export default AchieverContextPage;
