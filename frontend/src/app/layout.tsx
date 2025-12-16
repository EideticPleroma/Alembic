import type { Metadata } from 'next';
import { Inter, Cinzel } from 'next/font/google';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const cinzel = Cinzel({
  subsets: ['latin'],
  variable: '--font-cinzel',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'Alembic - Hermetic Tarot Mirror',
  description:
    'Transform questions into insight through the ancient wisdom of tarot. A vessel of transformation where synchronicity meets AI.',
  keywords: [
    'tarot',
    'hermetic',
    'tarot reading',
    'AI tarot',
    'depth psychology',
    'divination',
  ],
  authors: [{ name: 'Alembic' }],
  creator: 'Alembic',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://alembic.app',
    title: 'Alembic - Hermetic Tarot Mirror',
    description:
      'Transform questions into insight through the ancient wisdom of tarot.',
    siteName: 'Alembic',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Alembic - Hermetic Tarot Mirror',
    description:
      'Transform questions into insight through the ancient wisdom of tarot.',
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${cinzel.variable}`}
      suppressHydrationWarning
    >
      <head />
      <body className="min-h-screen bg-background font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
