'use client';

import Link from 'next/link';

export default function Privacy() {
  const sections = [
    {
      title: 'Information We Collect',
      content: `We collect information that you provide directly to us, information we obtain from your use of our services, and information from third parties. This includes:
        • Account information
        • Usage information
        • Device information
        • Location information
        • Information from third parties`
    },
    {
      title: 'How We Use Your Information',
      content: `We use the information we collect to:
        • Provide and maintain our services
        • Improve and develop new services
        • Communicate with you
        • Protect against fraud and abuse
        • Personalize your experience`
    },
    {
      title: 'Information Sharing',
      content: `We do not sell your personal information. We may share your information with:
        • Service providers
        • Business partners
        • Law enforcement when required
        • Other parties with your consent`
    },
    {
      title: 'Data Security',
      content: `We implement appropriate technical and organizational measures to protect your information, including:
        • Encryption of data in transit and at rest
        • Regular security assessments
        • Access controls and authentication
        • Employee training and confidentiality agreements`
    },
    {
      title: 'Your Rights',
      content: `You have certain rights regarding your personal information:
        • Access your data
        • Correct inaccurate data
        • Delete your data
        • Object to processing
        • Data portability`
    }
  ];

  return (
    <div className="min-h-screen py-20">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold mb-8">Privacy Policy</h1>
          <p className="text-xl text-gray-600 mb-12">
            Last updated: {new Date().toLocaleDateString()}
          </p>

          <div className="prose max-w-none">
            <p className="text-lg mb-8">
              At DocMatrix AI, we take your privacy seriously. This Privacy Policy explains how we collect, use, and protect your personal information when you use our services.
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
              <h2 className="text-2xl font-bold mb-4">Contact Us</h2>
              <p className="text-gray-600 mb-6">
                If you have any questions about this Privacy Policy, please contact us at:
              </p>
              <div className="bg-gray-50 p-6 rounded-lg">
                <p className="text-gray-600">
                  DocMatrix AI<br />
                  123 Tech Street<br />
                  Suite 456<br />
                  San Francisco, CA 94105<br />
                  United States<br />
                  <a
                    href="mailto:privacy@docmatrixai.com"
                    className="text-primary hover:text-primary-dark transition-colors"
                  >
                    privacy@docmatrixai.com
                  </a>
                </p>
              </div>
            </div>

            <div className="mt-12 flex justify-between items-center">
              <Link
                href="/legal/terms"
                className="text-primary hover:text-primary-dark transition-colors"
              >
                Terms of Service
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