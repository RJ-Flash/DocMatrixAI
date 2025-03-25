'use client';

import Link from 'next/link';

export default function Terms() {
  const sections = [
    {
      title: 'Acceptance of Terms',
      content: `By accessing or using DocMatrix AI's services, you agree to be bound by these Terms of Service and all applicable laws and regulations. If you do not agree with any of these terms, you are prohibited from using or accessing our services.`
    },
    {
      title: 'Use License',
      content: `Permission is granted to temporarily access and use DocMatrix AI's services for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:
        • Modify or copy the materials
        • Use the materials for any commercial purpose
        • Attempt to decompile or reverse engineer any software
        • Remove any copyright or other proprietary notations
        • Transfer the materials to another person or "mirror" the materials on any other server`
    },
    {
      title: 'Service Terms',
      content: `Our services are provided "as is." We make no warranties, expressed or implied, and hereby disclaim and negate all other warranties, including without limitation:
        • Implied warranties or merchantability
        • Fitness for a particular purpose
        • Non-infringement of intellectual property rights
        We do not guarantee that the services will be uninterrupted, timely, secure, or error-free.`
    },
    {
      title: 'Limitations',
      content: `In no event shall DocMatrix AI or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use our services, even if DocMatrix AI or an authorized representative has been notified orally or in writing of the possibility of such damage.`
    },
    {
      title: 'User Obligations',
      content: `As a user of our services, you agree to:
        • Provide accurate and complete information
        • Maintain the security of your account credentials
        • Notify us immediately of any unauthorized use
        • Not use the services for any illegal purposes
        • Comply with all applicable laws and regulations`
    }
  ];

  return (
    <div className="min-h-screen py-20">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold mb-8">Terms of Service</h1>
          <p className="text-xl text-gray-600 mb-12">
            Last updated: {new Date().toLocaleDateString()}
          </p>

          <div className="prose max-w-none">
            <p className="text-lg mb-8">
              Please read these Terms of Service carefully before using DocMatrix AI's services. These terms govern your access to and use of our services.
            </p>

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
              <h2 className="text-2xl font-bold mb-4">Changes to Terms</h2>
              <div className="bg-gray-50 p-6 rounded-lg">
                <p className="text-gray-600">
                  DocMatrix AI reserves the right to modify or replace these Terms of Service at any time. We will provide notice of any changes by posting the new Terms of Service on this page. Your continued use of the Service after any such changes constitutes your acceptance of the new Terms of Service.
                </p>
              </div>
            </div>

            <div className="mt-12">
              <h2 className="text-2xl font-bold mb-4">Contact Us</h2>
              <p className="text-gray-600 mb-6">
                If you have any questions about these Terms of Service, please contact us at:
              </p>
              <div className="bg-gray-50 p-6 rounded-lg">
                <p className="text-gray-600">
                  DocMatrix AI<br />
                  123 Tech Street<br />
                  Suite 456<br />
                  San Francisco, CA 94105<br />
                  United States<br />
                  <a
                    href="mailto:legal@docmatrixai.com"
                    className="text-primary hover:text-primary-dark transition-colors"
                  >
                    legal@docmatrixai.com
                  </a>
                </p>
              </div>
            </div>

            <div className="mt-12 flex justify-between items-center">
              <Link
                href="/legal/privacy"
                className="text-primary hover:text-primary-dark transition-colors"
              >
                Privacy Policy
              </Link>
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