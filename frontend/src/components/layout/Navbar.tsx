import { Bell, User, Search } from 'lucide-react';

export const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">Platform</div>
      <div className="navbar-actions">
        <Search className="icon" />
        <Bell className="icon" />
        <User className="icon" />
      </div>
    </nav>
  );
};