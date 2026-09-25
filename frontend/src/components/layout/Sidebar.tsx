import { Link } from 'react-router-dom';
import { LayoutDashboard, User, Briefcase, FileText, Target, BookOpen, Award } from 'lucide-react';

export const Sidebar = ({ role }: { role: string }) => {
  const studentLinks = [
    { label: 'Dashboard', to: `/student/dashboard`, icon: <LayoutDashboard /> },
    { label: 'Profile', to: `/student/profile`, icon: <User /> },
    { label: 'Assessments', to: `/student/assessments`, icon: <BookOpen /> },
    { label: 'Skill Profile', to: `/student/skills`, icon: <Award /> },
    { label: 'Skill Gaps', to: `/student/skill-gaps`, icon: <Target /> },
    { label: 'Jobs & Internships', to: `/student/jobs`, icon: <Briefcase /> },
    { label: 'Applications', to: `/student/applications`, icon: <FileText /> },
    { label: 'Achiever AI', to: `/student/achiever`, icon: <Target /> },
  ];

  const companyLinks = [
    { label: 'Dashboard', to: `/company/dashboard`, icon: <LayoutDashboard /> },
    { label: 'Jobs', to: `/company/jobs`, icon: <Briefcase /> },
  ];

  const links = role === 'COMPANY' ? companyLinks : studentLinks;

  return (
    <aside className="sidebar">
      <ul>
        {links.map((link, idx) => (
          <li key={idx}>
            <Link to={link.to} className="sidebar-link">
              {link.icon}
              <span>{link.label}</span>
            </Link>
          </li>
        ))}
      </ul>
    </aside>
  );
};