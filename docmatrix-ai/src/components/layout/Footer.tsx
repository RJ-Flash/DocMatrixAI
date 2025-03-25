'use client';

import Link from 'next/link';

const Footer = () => {
  return (
    <footer className="bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
          <div className="lg:col-span-2">
            <h4 className="font-bold text-xl mb-4">DocMatrix AI</h4>
            <p className="text-gray-600 mb-4">
              Transforming document workflows with AI-powered intelligence across industries.
            </p>
            <div className="flex gap-4">
              {[
                { href: 'https://twitter.com/docmatrixai', label: 'Twitter' },
                { href: 'https://linkedin.com/company/docmatrixai', label: 'LinkedIn' },
                { href: 'https://facebook.com/docmatrixai', label: 'Facebook' }
              ].map((social) => (
                <Link
                  key={social.label}
                  href={social.href}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                  aria-label={`Visit our ${social.label} page`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <span className="sr-only">{social.label}</span>
                  {social.label === 'Twitter' && (
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                    </svg>
                  )}
                </Link>
              ))}
            </div>
          </div>

          <div>
            <h5 className="font-bold mb-4">Products</h5>
            <ul className="space-y-2">
              {[
                { href: '/products/ContractAI', label: 'ContractAI' },
                { href: '/products/ExpenseDocAI', label: 'ExpenseDocAI' },
                { href: '/products/HR-DocAI', label: 'HR-DocAI' },
                { href: '/products/SupplyDocAI', label: 'SupplyDocAI' }
              ].map((product) => (
                <li key={product.label}>
                  <Link
                    href={product.href}
                    className="text-gray-600 hover:text-gray-900 transition-colors"
                    aria-label={`Learn more about ${product.label}`}
                  >
                    {product.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h5 className="font-bold mb-4">Resources</h5>
            <ul className="space-y-2">
              {[
                { href: '/resources/documentation', label: 'Documentation' },
                { href: '/resources/api-reference', label: 'API Reference' },
                { href: '/resources/blog', label: 'Blog' },
                { href: '/resources/case-studies', label: 'Case Studies' }
              ].map((resource) => (
                <li key={resource.label}>
                  <Link
                    href={resource.href}
                    className="text-gray-600 hover:text-gray-900 transition-colors"
                    aria-label={`View our ${resource.label}`}
                  >
                    {resource.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h5 className="font-bold mb-4">Company</h5>
            <ul className="space-y-2">
              {[
                { href: '/company/about', label: 'About Us' },
                { href: '/company/careers', label: 'Careers' },
                { href: '/company/partners', label: 'Partners' },
                { href: '/company/contact', label: 'Contact' }
              ].map((item) => (
                <li key={item.label}>
                  <Link
                    href={item.href}
                    className="text-gray-600 hover:text-gray-900 transition-colors"
                    aria-label={item.label}
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <hr className="my-8 border-gray-200" />

        <div className="flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-600 mb-4 md:mb-0">
            © {new Date().getFullYear()} DocMatrix AI. All rights reserved.
          </p>
          <div className="flex gap-6">
            {[
              { href: '/legal/privacy', label: 'Privacy Policy' },
              { href: '/legal/terms', label: 'Terms of Service' },
              { href: '/legal/security', label: 'Security' }
            ].map((link) => (
              <Link
                key={link.label}
                href={link.href}
                className="text-gray-600 hover:text-gray-900 transition-colors"
                aria-label={`Read our ${link.label}`}
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 