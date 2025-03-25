'use client';

import Link from 'next/link';

export default function APIReference() {
  const apiSections = [
    {
      title: 'Authentication',
      description: 'Learn how to authenticate your API requests.',
      endpoint: '/api/v1/auth',
      method: 'POST',
      links: [
        { href: '/resources/api-reference/authentication', label: 'Authentication Guide' },
        { href: '/resources/api-reference/tokens', label: 'API Tokens' }
      ]
    },
    {
      title: 'Document Processing',
      description: 'Endpoints for processing and analyzing documents.',
      endpoint: '/api/v1/documents',
      method: 'POST',
      links: [
        { href: '/resources/api-reference/documents', label: 'Document API' },
        { href: '/resources/api-reference/analysis', label: 'Analysis API' }
      ]
    },
    {
      title: 'Integration',
      description: 'Integrate DocMatrix AI with your existing systems.',
      endpoint: '/api/v1/integrate',
      method: 'POST',
      links: [
        { href: '/resources/api-reference/webhooks', label: 'Webhooks' },
        { href: '/resources/api-reference/events', label: 'Events' }
      ]
    }
  ];

  return (
    <div className="min-h-screen py-20">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold mb-8">API Reference</h1>
          <p className="text-xl text-gray-600 mb-12">
            Complete reference documentation for the DocMatrix AI API.
          </p>

          <div className="space-y-8">
            {apiSections.map((section) => (
              <div key={section.title} className="bg-white rounded-lg shadow-lg overflow-hidden">
                <div className="p-6">
                  <h2 className="text-2xl font-bold mb-4">{section.title}</h2>
                  <p className="text-gray-600 mb-6">{section.description}</p>
                  
                  <div className="bg-gray-50 rounded-lg p-4 mb-6 font-mono text-sm">
                    <div className="flex items-center space-x-2">
                      <span className="px-2 py-1 bg-primary text-white rounded text-xs">
                        {section.method}
                      </span>
                      <span className="text-gray-700">{section.endpoint}</span>
                    </div>
                  </div>

                  <ul className="space-y-3">
                    {section.links.map((link) => (
                      <li key={link.label}>
                        <Link
                          href={link.href}
                          className="text-primary hover:text-primary-dark transition-colors flex items-center"
                        >
                          <svg
                            className="w-4 h-4 mr-2"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M9 5l7 7-7 7"
                            />
                          </svg>
                          {link.label}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-12 p-6 bg-primary text-white rounded-lg">
            <h2 className="text-2xl font-bold mb-4">Need API Support?</h2>
            <p className="mb-6">
              Having trouble with our API? Our developer support team is here to help.
            </p>
            <div className="flex gap-4">
              <Link
                href="/company/contact"
                className="inline-block bg-white text-primary px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                Contact Support
              </Link>
              <Link
                href="/resources/documentation"
                className="inline-block border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-primary transition-colors"
              >
                View Documentation
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 