export const Role = {
  STUDENT: 'STUDENT',
  COMPANY: 'COMPANY',
  MENTOR: 'MENTOR',
  TPO: 'TPO',
  ADMIN: 'ADMIN'
} as const;

export const getDashboardRoute = (role?: string): string => {
  switch (role) {
    case Role.STUDENT:
      return '/student/onboarding'; // Auto-redirects to dashboard if complete
    case 'student': // Handle lowercase gracefully
      return '/student/onboarding';
    default:
      // Fallback for roles without an implemented dashboard or unknown roles
      return '/';
  }
};
