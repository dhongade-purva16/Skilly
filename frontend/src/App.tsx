
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import { StudentLayout } from './layouts/StudentLayout';
import { StudentDashboard } from './pages/student/Dashboard';
import { Profile } from './pages/student/Profile';
import { SkillProfile } from './pages/student/SkillProfile';
import { SkillGaps } from './pages/student/SkillGaps';
import { Assessments } from './pages/student/Assessments';
import { AssessmentAttempt } from './pages/student/AssessmentAttempt';
import { Onboarding } from './pages/student/Onboarding';
import { Landing } from './pages/auth/Landing';
import { Login } from './pages/auth/Login';
import { Register } from './pages/auth/Register';
import AchieverContextPage from './pages/student/AchieverContextPage';
import GemsPage from './pages/student/GemsPage';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { AuthProvider } from './contexts/AuthContext';
import { CompanyLayout } from './layouts/CompanyLayout';
import { StudentJobs } from './pages/student/StudentJobs';
import { StudentApplications } from './pages/student/StudentApplications';
import { CompanyDashboard } from './pages/company/CompanyDashboard';
import { CompanyJobs } from './pages/company/CompanyJobs';
import { CompanyJobCreate } from './pages/company/CompanyJobCreate';
import { CompanyJobDetails } from './pages/company/CompanyJobDetails';
import { CompanyApplicants } from './pages/company/CompanyApplicants';
import { CompanyAssessmentBuilder } from './pages/company/CompanyAssessmentBuilder';
import { StudentJobDetails } from './pages/student/StudentJobDetails';
import { StudentAssessmentView } from './pages/student/StudentAssessmentView';
const App = () => {
  return (
    <AuthProvider>

      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Student Routes */}
          <Route path="/student" element={<ProtectedRoute />}>
            <Route path="onboarding" element={<Onboarding />} />
            <Route element={<StudentLayout />}>
              <Route path="dashboard" element={<StudentDashboard />} />
              <Route path="profile" element={<Profile />} />
              <Route path="skills" element={<SkillProfile />} />
              <Route path="skill-gaps" element={<SkillGaps />} />
              <Route path="assessments" element={<Assessments />} />
              <Route path="assessments/:id" element={<AssessmentAttempt />} />
              <Route path="achiever" element={<AchieverContextPage />} />
              <Route path="gems" element={<GemsPage />} />
              <Route path="jobs" element={<StudentJobs />} />
              <Route path="jobs/:jobId" element={<StudentJobDetails />} />
              <Route path="internships" element={<StudentJobs />} />
              <Route path="applications" element={<StudentApplications />} />
              <Route path="applications/:applicationId/assessment" element={<StudentAssessmentView />} />
            </Route>
          </Route>

          {/* Company Routes */}
          <Route path="/company" element={<ProtectedRoute />}>
            <Route element={<CompanyLayout />}>
              <Route path="dashboard" element={<CompanyDashboard />} />
              <Route path="jobs" element={<CompanyJobs />} />
              <Route path="jobs/new" element={<CompanyJobCreate />} />
              <Route path="jobs/:jobId" element={<CompanyJobDetails />} />
              <Route path="jobs/:jobId/applicants" element={<CompanyApplicants />} />
              <Route path="jobs/:jobId/assessment" element={<CompanyAssessmentBuilder />} />
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;