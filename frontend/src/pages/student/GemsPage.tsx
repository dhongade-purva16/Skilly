import React, { useEffect, useState } from 'react';
import { getDailyPlan, startGemsTask, completeGemsTask, skipGemsTask, rescheduleGemsTask, getGemsTaskHelp } from '../../services/gems';
import type { GemsDailyPlanResponse, HelpContextResponse } from '../../services/gems';
import './GemsPage.css';

const GemsPage: React.FC = () => {
  const [plan, setPlan] = useState<GemsDailyPlanResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [helpData, setHelpData] = useState<Record<number, HelpContextResponse>>({});
  const [actionLoading, setActionLoading] = useState<number | null>(null);

  const fetchPlan = async () => {
    try {
      setLoading(true);
      const data = await getDailyPlan();
      setPlan(data);
      setError(null);
    } catch (err) {
      console.error('Failed to load GEMS daily plan', err);
      setError('Failed to load GEMS Daily Plan.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlan();
  }, []);

  const handleAction = async (taskId: number, action: string) => {
    try {
      setActionLoading(taskId);
      if (action === 'start') {
        await startGemsTask(taskId);
      } else if (action === 'complete') {
        await completeGemsTask(taskId, 'Completed from UI');
      } else if (action === 'skip') {
        await skipGemsTask(taskId, 'Skipped from UI');
      } else if (action === 'reschedule') {
        await rescheduleGemsTask(taskId);
      } else {
        return;
      }

      // Update the local state
      if (plan) {
        // Recalculate summary locally or refetch
        fetchPlan();
      }
    } catch (err) {
      console.error(`Failed to ${action} task`, err);
      alert(`Failed to ${action} task.`);
    } finally {
      setActionLoading(null);
    }
  };

  const handleHelp = async (taskId: number) => {
    try {
      setActionLoading(taskId);
      const data = await getGemsTaskHelp(taskId);
      setHelpData(prev => ({ ...prev, [taskId]: data }));
    } catch (err) {
      console.error('Failed to load help context', err);
      alert('Failed to load help resources.');
    } finally {
      setActionLoading(null);
    }
  };

  if (loading) return <div className="gems-loading">Loading GEMS Plan...</div>;
  if (error) return <div className="gems-error">{error}</div>;

  if (!plan || !plan.tasks.length) {
    return (
      <div className="gems-page">
        <header className="gems-header">
          <h1>GEMS</h1>
          <p className="subtitle">Your Daily Career Plan</p>
        </header>
        <div className="gems-card">
          <p>You have no active roadmap or daily plan today. Please generate a personalized roadmap first.</p>
        </div>
      </div>
    );
  }

  const completionPercentage = plan.summary.total > 0 ? Math.round((plan.summary.completed / plan.summary.total) * 100) : 0;

  return (
    <div className="gems-page">
      <header className="gems-header">
        <h1>GEMS</h1>
        <p className="subtitle">Your Daily Career Plan</p>
      </header>

      <div className="gems-grid">
        <section className="gems-card progress-section">
          <h2 style={{margin: '0 0 1rem 0'}}>Today's Progress - {plan.plan_date}</h2>
          
          <div className="progress-stats">
            <div className="stat-box">
              <span className="stat-value">{plan.summary.completed} / {plan.summary.total}</span>
              <span className="stat-label">Completed</span>
            </div>
            <div className="stat-box">
              <span className="stat-value">{plan.summary.remaining}</span>
              <span className="stat-label">Remaining</span>
            </div>
            <div className="stat-box">
              <span className="stat-value">{plan.summary.estimated_remaining_minutes}</span>
              <span className="stat-label">Est. Min Left</span>
            </div>
          </div>

          <div className="progress-bar-container">
            <div className="progress-bar-fill" style={{ width: `${completionPercentage}%` }}></div>
          </div>
          <p className="progress-text">{completionPercentage}% Completed</p>
        </section>

        <section className="gems-card full-width">
          <h2 style={{margin: '0 0 1rem 0'}}>TODAY'S TASKS</h2>
          <div className="gems-tasks">
            {plan.tasks.map((task) => (
              <div key={task.id} className={`gems-task-card ${task.status}`}>
                <div className="task-header">
                  <div className="task-title-area">
                    {task.status === 'completed' ? (
                      <span className="task-checkbox checked">✓</span>
                    ) : task.status === 'in_progress' ? (
                      <span className="task-checkbox in-progress">▶</span>
                    ) : (
                      <span className="task-checkbox empty"></span>
                    )}
                    <h3 className="task-title">{task.title}</h3>
                  </div>
                  <span className={`status-badge ${task.status.replace('_', '-')}`}>{task.status.replace('_', ' ').toUpperCase()}</span>
                </div>
                
                <div className="task-meta">
                  <span className="meta-tag">{task.skill_name}</span>
                  <span className="meta-tag">{task.estimated_minutes} min</span>
                  <span className={`meta-tag priority-${task.priority.toLowerCase()}`}>{task.priority}</span>
                  <span className="meta-tag type">{task.task_type}</span>
                </div>
                
                <p className="task-desc">{task.description}</p>
                
                {task.status !== 'completed' && task.status !== 'skipped' && task.status !== 'rescheduled' && (
                  <div className="task-actions">
                    {task.status === 'not_started' && (
                      <button className="btn-action primary" onClick={() => handleAction(task.id, 'start')} disabled={actionLoading === task.id}>
                        {actionLoading === task.id ? '...' : 'Start'}
                      </button>
                    )}
                    {task.status === 'in_progress' && (
                      <button className="btn-action success" onClick={() => handleAction(task.id, 'complete')} disabled={actionLoading === task.id}>
                        {actionLoading === task.id ? '...' : 'Complete'}
                      </button>
                    )}
                    <button className="btn-action secondary" onClick={() => handleAction(task.id, 'reschedule')} disabled={actionLoading === task.id}>Do Later</button>
                    <button className="btn-action secondary" onClick={() => handleAction(task.id, 'skip')} disabled={actionLoading === task.id}>Skip</button>
                    <button className="btn-action secondary help" onClick={() => handleHelp(task.id)} disabled={actionLoading === task.id}>Need Help</button>
                  </div>
                )}
                
                {helpData[task.id] && (
                  <div className="task-help-area">
                    <h4>Recommended Resources for this Task:</h4>
                    {helpData[task.id].resources.length > 0 ? (
                      <ul>
                        {helpData[task.id].resources.map(r => (
                          <li key={r.resource_id}>
                            <a href={r.source_url} target="_blank" rel="noreferrer">{r.title}</a> ({r.provider})
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p>No resources attached to this task. Please consult external docs.</p>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

export default GemsPage;
