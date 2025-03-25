'use client';

import Link from 'next/link';

export default function Security() {
  const sections = [
    {
      title: 'Security Overview',
      content: `At DocMatrix AI, security is our top priority. We employ industry-leading security measures to protect your data and maintain the trust you place in us. Our comprehensive security program includes:
        • SOC 2 Type II compliance
        • ISO 27001 certification
        • Regular third-party security audits
        • Continuous security monitoring`
    },
    {
      title: 'Data Protection',
      content: `We implement multiple layers of security to protect your data:
        • AES-256 encryption for data at rest
        • TLS 1.3 for data in transit
        • Regular backup procedures
        • Secure data centers with redundancy
        • Strict access controls and authentication`
    },
    {
      title: 'Infrastructure Security',
      content: `Our infrastructure is built on secure foundations:
        • Cloud security best practices
        • Network segmentation
        • Firewalls and intrusion detection
        • DDoS protection
        • Regular vulnerability scanning`
    },
    {
      title: 'Access Control',
      content: `We maintain strict access controls:
        • Multi-factor authentication
        • Role-based access control (RBAC)
        • Regular access reviews
        • Audit logging
        • Session management`
    },
    {
      title: 'Compliance',
      content: `We maintain compliance with major security standards:
        • GDPR
        • CCPA
        • HIPAA (where applicable)
        • PCI DSS
        • SOX compliance`
    }
  ];

  return (
    <div className="min-h-screen py-20">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold mb-8">Security</h1>
          <p className="text-xl text-gray-600 mb-12">
            Our commitment to protecting your data and maintaining trust
          </p>

          <div className="prose max-w-none">
            <div className="space-y-12">
              {sections.map((section) => (
                <div key={section.title}>
                  <h2 className="text-2xl font-bold mb-4">{section.title}</h2>
                  <div className="bg-white rounded-lg shadow-lg p-6">
                    <p className="whitespace-pre-line text-gray-600">
                      {section.content}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-12">
              <h2 className="text-2xl font-bold mb-4">Security Reporting</h2>
              <div className="bg-primary text-white p-6 rounded-lg">
                <h3 className="text-xl font-bold mb-4">Responsible Disclosure</h3>
                <p className="mb-4">
                  We appreciate the work of security researchers in helping keep our platform secure. If you believe you've found a security vulnerability, please report it to us responsibly.
                </p>
                <a
                  href="mailto:security@docmatrixai.com"
                  className="inline-block bg-white text-primary px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
                >
                  Report a Vulnerability
                </a>
              </div>
            </div>

            <div className="mt-12">
              <h2 className="text-2xl font-bold mb-4">Contact Security Team</h2>
              <div className="bg-gray-50 p-6 rounded-lg">
                <p className="text-gray-600">
                  For security-related inquiries, please contact our security team at:
                </p>
                <p className="mt-4">
                  <a
                    href="mailto:security@docmatrixai.com"
                    className="text-primary hover:text-primary-dark transition-colors"
                  >
                    security@docmatrixai.com
                  </a>
                </p>
                <p className="mt-4 text-gray-600">
                  For urgent security matters, please include "URGENT" in the subject line.
                </p>
              </div>
            </div>

            <div className="mt-12 flex justify-between items-center">
              <div className="space-x-6">
                <Link
                  href="/legal/privacy"
                  className="text-primary hover:text-primary-dark transition-colors"
                >
                  Privacy Policy
                </Link>
                <Link
                  href="/legal/terms"
                  className="text-primary hover:text-primary-dark transition-colors"
                >
                  Terms of Service
                </Link>
              </div>
              <Link
                href="/company/contact"
                className="bg-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-dark transition-colors"
              >
                Contact Us
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 