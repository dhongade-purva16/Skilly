import { useEffect, useState } from 'react';
import { Card } from '../../components/ui/Card';
import { 
  getAssessment, 
  startAttempt, 
  submitAttempt,
  type AssessmentDetail,
  type AssessmentResult
} from '../../services/assessment';
import { useParams, useNavigate } from 'react-router-dom';
import './AssessmentAttempt.css';

export const AssessmentAttempt = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [assessment, setAssessment] = useState<AssessmentDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const [attemptId, setAttemptId] = useState<number | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<AssessmentResult | null>(null);

  useEffect(() => {
    const fetchAssessment = async () => {
      try {
        setLoading(true);
        if (!id) return;
        const data = await getAssessment(parseInt(id));
        setAssessment(data);
      } catch (err) {
        setError('Failed to load assessment details.');
      } finally {
        setLoading(false);
      }
    };
    fetchAssessment();
  }, [id]);

  const handleStart = async () => {
    try {
      setError(null);
      const res = await startAttempt(assessment!.id);
      setAttemptId(res.id);
    } catch (err) {
      setError('Failed to start assessment attempt.');
    }
  };

  const handleSelectOption = (questionId: number, optionIndex: number) => {
    setAnswers({
      ...answers,
      [questionId]: optionIndex
    });
  };

  const handleNext = () => {
    if (currentQuestionIndex < (assessment?.questions.length || 0) - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handlePrev = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleSubmit = async () => {
    if (!attemptId || !assessment) return;
    
    // Check if all answered
    if (Object.keys(answers).length < assessment.questions.length) {
      const confirmSubmit = window.confirm('You have unanswered questions. Are you sure you want to submit?');
      if (!confirmSubmit) return;
    }

    try {
      setSubmitting(true);
      setError(null);
      
      const formattedAnswers = Object.entries(answers).map(([qId, oIdx]) => ({
        question_id: parseInt(qId),
        selected_option_index: oIdx
      }));

      const res = await submitAttempt(attemptId, { answers: formattedAnswers });
      setResult(res);
    } catch (err) {
      setError('Failed to submit assessment.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="page loading">Loading...</div>;
  if (error) return <div className="page error"><div className="alert error">{error}</div></div>;
  if (!assessment) return <div className="page error">Assessment not found.</div>;

  // View: Result Screen
  if (result) {
    return (
      <div className="page attempt-page">
        <Card className="result-card">
          <h2>Assessment Complete!</h2>
          <div className="score-display">
            <span className="score-value">{result.score.toFixed(1)}%</span>
            <span className="score-label">Score</span>
          </div>
          <p>Your skill profile has been updated based on this result.</p>
          <div className="form-actions" style={{ justifyContent: 'center' }}>
            <button className="btn-primary" onClick={() => navigate('/student/skills')}>
              View Skill Profile
            </button>
          </div>
        </Card>
      </div>
    );
  }

  // View: Instruction Screen
  if (!attemptId) {
    return (
      <div className="page attempt-page">
        <Card className="instruction-card">
          <h2>{assessment.title}</h2>
          <div className="skill-tag">{assessment.skill.name}</div>
          <div className="instructions-content">
            <p>{assessment.description}</p>
            <ul>
              <li><strong>Questions:</strong> {assessment.questions.length}</li>
              <li><strong>Evaluation:</strong> Automatic grading after submission</li>
              <li><strong>Note:</strong> You cannot pause the assessment once started.</li>
            </ul>
          </div>
          <div className="form-actions" style={{ justifyContent: 'flex-start' }}>
            <button className="btn-primary" onClick={handleStart}>
              Start Assessment
            </button>
            <button className="btn-secondary ml-4" onClick={() => navigate('/student/assessments')}>
              Cancel
            </button>
          </div>
        </Card>
      </div>
    );
  }

  // View: Questions
  const currentQuestion = assessment.questions[currentQuestionIndex];
  const isLastQuestion = currentQuestionIndex === assessment.questions.length - 1;

  return (
    <div className="page attempt-page">
      <div className="progress-indicator">
        Question {currentQuestionIndex + 1} of {assessment.questions.length}
      </div>
      
      <Card className="question-card">
        <h3>{currentQuestion.question_text}</h3>
        <div className="options-list">
          {currentQuestion.options.map((opt: string, idx: number) => (
            <label 
              key={idx} 
              className={`option-label ${answers[currentQuestion.id] === idx ? 'selected' : ''}`}
            >
              <input 
                type="radio" 
                name={`question-${currentQuestion.id}`}
                value={idx}
                checked={answers[currentQuestion.id] === idx}
                onChange={() => handleSelectOption(currentQuestion.id, idx)}
              />
              <span className="option-text">{opt}</span>
            </label>
          ))}
        </div>
      </Card>
      
      <div className="attempt-navigation">
        <button 
          className="btn-secondary" 
          onClick={handlePrev} 
          disabled={currentQuestionIndex === 0}
        >
          Previous
        </button>
        
        {isLastQuestion ? (
          <button 
            className="btn-primary" 
            onClick={handleSubmit} 
            disabled={submitting}
          >
            {submitting ? 'Submitting...' : 'Submit Assessment'}
          </button>
        ) : (
          <button 
            className="btn-primary" 
            onClick={handleNext}
          >
            Next
          </button>
        )}
      </div>
    </div>
  );
};
