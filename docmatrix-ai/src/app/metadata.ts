import { Metadata } from 'next';

const defaultMetadata: Metadata = {
  title: {
    default: 'DocMatrix AI - AI-Powered Document Intelligence Platform',
    template: '%s | DocMatrix AI'
  },
  description: 'Transform your document workflows with AI-powered intelligence. DocMatrix AI helps enterprises automate document processing with up to 85% time savings.',
  keywords: [
    'AI document processing',
    'document automation',
    'contract analysis',
    'expense processing',
    'HR document management',
    'supply chain documentation',
    'artificial intelligence',
    'machine learning',
    'enterprise software'
  ],
  authors: [{ name: 'DocMatrix AI' }],
  creator: 'DocMatrix AI',
  publisher: 'DocMatrix AI',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://docmatrixai.com',
    siteName: 'DocMatrix AI',
    title: 'DocMatrix AI - AI-Powered Document Intelligence Platform',
    description: 'Transform your document workflows with AI-powered intelligence. DocMatrix AI helps enterprises automate document processing with up to 85% time savings.',
    images: [
      {
        url: '/images/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'DocMatrix AI Platform'
      }
    ]
  },
  twitter: {
    card: 'summary_large_image',
    title: 'DocMatrix AI - AI-Powered Document Intelligence Platform',
    description: 'Transform your document workflows with AI-powered intelligence. DocMatrix AI helps enterprises automate document processing with up to 85% time savings.',
    images: ['/images/twitter-image.jpg'],
    creator: '@docmatrixai'
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png',
  },
  manifest: '/site.webmanifest',
  verification: {
    google: 'your-google-site-verification',
    yandex: 'your-yandex-verification',
    bing: 'your-bing-verification'
  }
};

export default defaultMetadata; 