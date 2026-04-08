import type { Metadata, Viewport } from 'next'
import { Inter, Poppins } from 'next/font/google'
import './globals.css'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const poppins = Poppins({
  subsets: ['latin'],
  weight: ['400', '600', '700'],
  variable: '--font-poppins',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Chapter DNA',
  description: 'Discover what makes your Pavilion chapter tick.',
  metadataBase: new URL('https://chapter-dna.vercel.app'),
  openGraph: {
    title: 'Chapter DNA',
    description: 'Discover what makes your Pavilion chapter tick.',
    type: 'website',
  },
}

export const viewport: Viewport = {
  themeColor: '#180A5C',
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${poppins.variable}`}>
      <body className="bg-[#180A5C] text-white font-sans">
        <main className="mx-auto max-w-md min-h-dvh">
          {children}
        </main>
      </body>
    </html>
  )
}
