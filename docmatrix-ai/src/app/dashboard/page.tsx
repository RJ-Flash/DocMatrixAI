'use client';

import { useState } from 'react';
import ProtectedRoute from '@/components/shared/ProtectedRoute';
import { useForm } from '@/hooks/useForm';
import { useApi } from '@/hooks/useApi';
import { useNotificationStore } from '@/store/notificationStore';
import { useAuthStore } from '@/store/authStore';

interface TestFormData {
  title: string;
  description: string;
}

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState<'form' | 'api' | 'notifications'>('form');
  const addNotification = useNotificationStore((state) => state.addNotification);
  const user = useAuthStore((state) => state.user);

  // Form Test
  const { values, errors, isSubmitting, handleChange, handleSubmit } = useForm<TestFormData>(
    {
      title: '',
      description: '',
    },
    {
      title: { required: true, minLength: 3 },
      description: { required: true, minLength: 10 },
    },
    async (values) => {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000));
      addNotification({
        type: 'success',
        message: 'Form submitted successfully!',
        duration: 3000,
      });
      console.log('Form values:', values);
    }
  );

  // API Test
  const { data, error, isLoading, execute } = useApi('/api/test');

  const handleApiTest = async () => {
    try {
      await execute({
        method: 'POST',
        body: { test: true },
      });
      addNotification({
        type: 'success',
        message: 'API call successful!',
        duration: 3000,
      });
    } catch {
      // Error is handled by useApi hook
    }
  };

  // Notification Test
  const handleNotificationTest = () => {
    ['success', 'error', 'info'].forEach((type, index) => {
      setTimeout(() => {
        addNotification({
          type: type as 'success' | 'error' | 'info',
          message: `This is a ${type} notification!`,
          duration: 3000,
        });
      }, index * 1000);
    });
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen py-12 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
              <h1 className="text-2xl font-bold mb-4">Welcome, {user?.firstName}!</h1>
              <p className="text-gray-600">
                This is a test dashboard demonstrating our implemented features.
              </p>
            </div>

            {/* Tab Navigation */}
            <div className="flex mb-6 space-x-4">
              {(['form', 'api', 'notifications'] as const).map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-4 py-2 rounded-lg font-medium ${
                    activeTab === tab
                      ? 'bg-primary text-white'
                      : 'bg-white text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  {tab.charAt(0).toUpperCase() + tab.slice(1)} Test
                </button>
              ))}
            </div>

            {/* Tab Content */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              {activeTab === 'form' && (
                <div>
                  <h2 className="text-xl font-bold mb-4">Form Handling Test</h2>
                  <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Title
                      </label>
                      <input
                        type="text"
                        name="title"
                        value={values.title}
                        onChange={handleChange}
                        className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent ${
                          errors.title ? 'border-red-500' : 'border-gray-300'
                        }`}
                      />
                      {errors.title && (
                        <p className="text-red-500 text-sm mt-1">{errors.title}</p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Description
                      </label>
                      <textarea
                        name="description"
                        value={values.description}
                        onChange={handleChange}
                        rows={3}
                        className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent ${
                          errors.description ? 'border-red-500' : 'border-gray-300'
                        }`}
                      />
                      {errors.description && (
                        <p className="text-red-500 text-sm mt-1">{errors.description}</p>
                      )}
                    </div>

                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className="w-full bg-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-dark transition-colors disabled:opacity-50"
                    >
                      {isSubmitting ? 'Submitting...' : 'Submit Form'}
                    </button>
                  </form>
                </div>
              )}

              {activeTab === 'api' && (
                <div>
                  <h2 className="text-xl font-bold mb-4">API Test</h2>
                  <div className="space-y-4">
                    <button
                      onClick={handleApiTest}
                      disabled={isLoading}
                      className="w-full bg-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-dark transition-colors disabled:opacity-50"
                    >
                      {isLoading ? 'Loading...' : 'Test API Call'}
                    </button>
                    {error && (
                      <div className="p-4 bg-red-50 text-red-600 rounded-lg">
                        {error.message}
                      </div>
                    )}
                    {data && (
                      <div className="p-4 bg-green-50 text-green-600 rounded-lg">
                        API Response: {JSON.stringify(data)}
                      </div>
                    )}
                  </div>
                </div>
              )}

              {activeTab === 'notifications' && (
                <div>
                  <h2 className="text-xl font-bold mb-4">Notifications Test</h2>
                  <button
                    onClick={handleNotificationTest}
                    className="w-full bg-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-dark transition-colors"
                  >
                    Show Test Notifications
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
} 