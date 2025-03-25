'use client';

import { useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';

const publicPaths = [
  '/',
  '/login',
  '/signup',
  '/forgot-password',
  '/legal/privacy',
  '/legal/terms',
  '/legal/security',
];

export default function AuthProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const token = useAuthStore((state) => state.token);

  useEffect(() => {
    // Check if the current path requires authentication
    const isPublicPath = publicPaths.includes(pathname) || 
      pathname.startsWith('/products/') ||
      pathname.startsWith('/company/');

    if (!token && !isPublicPath) {
      router.push('/login');
    }
  }, [pathname, token, router]);

  return <>{children}</>;
} 