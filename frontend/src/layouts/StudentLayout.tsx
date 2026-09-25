import { Outlet } from 'react-router-dom';
import { Navbar } from '../components/layout/Navbar';
import { Sidebar } from '../components/layout/Sidebar';

export const StudentLayout = () => {
  return (
    <div className="app-shell">
      <Navbar />
      <div className="app-body">
        <Sidebar role="STUDENT" />
        <main className="main-content"><Outlet /></main>
      </div>
    </div>
  );
};