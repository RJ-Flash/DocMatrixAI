'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import LoadingSpinner from './LoadingSpinner';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: 'user' | 'admin';
}

export default function ProtectedRoute({
  children,
  requiredRole,
}: ProtectedRouteProps) {
  const router = useRouter();
  const { user, token, isLoading } = useAuthStore();

  useEffect(() => {
    if (!isLoading && !token) {
      router.push('/login');
      return;
    }

    if (requiredRole && user?.role !== requiredRole) {
      router.push('/unauthorized');
    }
  }, [isLoading, token, user, requiredRole, router]);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!token || (requiredRole && user?.role !== requiredRole)) {
    return null;
  }

  return <>{children}</>;
} 