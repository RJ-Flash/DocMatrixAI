'use client';

import Link from 'next/link';

interface ProductCardProps {
  title: string;
  description: string;
  category: string;
  timeSaving: string;
  href: string;
  icon: React.ReactNode;
}

const ProductCard = ({
  title,
  description,
  category,
  timeSaving,
  href,
  icon,
}: ProductCardProps) => {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 h-full flex flex-col">
      <span className="inline-block px-3 py-1 rounded-full text-sm font-medium bg-primary/10 text-primary mb-4">
        {category}
      </span>
      <div className="text-primary mb-4">
        {icon}
      </div>
      <h3 className="text-xl font-bold mb-3">{title}</h3>
      <p className="text-gray-600 mb-4 flex-grow">{description}</p>
      <div className="flex items-center justify-between mt-auto">
        <Link
          href={href}
          className="font-semibold text-primary hover:text-primary-dark transition-colors"
          aria-label={`Learn more about ${title}`}
        >
          Learn More
        </Link>
        <span className="badge bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm">
          {timeSaving} Time Savings
        </span>
      </div>
    </div>
  );
};

export default ProductCard; 