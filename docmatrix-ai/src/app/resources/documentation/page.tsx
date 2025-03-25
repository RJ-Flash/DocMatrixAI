'use client';

import Link from 'next/link';

export default function Documentation() {
  const docs = [
    {
      title: 'Getting Started',
      description: 'Learn the basics of DocMatrix AI and how to get started with our platform.',
      links: [
        { href: '/resources/documentation/quickstart', label: 'Quick Start Guide' },
        { href: '/resources/documentation/installation', label: 'Installation' },
        { href: '/resources/documentation/configuration', label: 'Configuration' }
      ]
    },
    {
      title: 'Product Documentation',
      description: 'Detailed documentation for each DocMatrix AI product.',
      links: [
        { href: '/products/ContractAI', label: 'ContractAI Documentation' },
        { href: '/products/ExpenseDocAI', label: 'ExpenseDocAI Documentation' },
        { href: '/products/HR-DocAI', label: 'HR-DocAI Documentation' },
        { href: '/products/SupplyDocAI', label: 'SupplyDocAI Documentation' }
      ]
    },
    {
      title: 'API Reference',
      description: 'Complete API documentation for developers.',
      links: [
        { href: '/resources/api-reference', label: 'API Overview' },
        { href: '/resources/api-reference/authentication', label: 'Authentication' },
        { href: '/resources/api-reference/endpoints', label: 'API Endpoints' }
      ]
    }
  ];

  return (
    <div className="min-h-screen py-20">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold mb-8">Documentation</h1>
          <p className="text-xl text-gray-600 mb-12">
            Everything you need to know about DocMatrix AI's products and services.
          </p>

          <div className="space-y-12">
            {docs.map((section) => (
              <div key={section.title} className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold mb-4">{section.title}</h2>
                <p className="text-gray-600 mb-6">{section.description}</p>
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
            ))}
          </div>

          <div className="mt-12 p-6 bg-primary text-white rounded-lg">
            <h2 className="text-2xl font-bold mb-4">Need Help?</h2>
            <p className="mb-6">
              Can't find what you're looking for? Our support team is here to help.
            </p>
            <Link
              href="/company/contact"
              className="inline-block bg-white text-primary px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
            >
              Contact Support
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
} 