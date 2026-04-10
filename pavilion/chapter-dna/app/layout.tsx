import type { Metadata, Viewport } from 'next'
import { Inter, Poppins, Space_Grotesk } from 'next/font/google'
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

const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700', '800', '900'],
  variable: '--font-space-grotesk',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Chapter Wars by Pavilion',
  description: '15 cities. 6 archetypes. One winner.',
  metadataBase: new URL('https://chapter-dna.vercel.app'),
  openGraph: {
    title: 'Chapter Wars by Pavilion',
    description: '15 cities. 6 archetypes. One winner.',
    type: 'website',
  },
}

export const viewport: Viewport = {
  themeColor: '#FFE135',
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
    <html lang="en" className={`${inter.variable} ${poppins.variable} ${spaceGrotesk.variable}`}>
      <body className="bg-cw-charcoal text-white font-sans">
        <main className="mx-auto max-w-md min-h-dvh">
          {children}
        </main>
      </body>
    </html>
  )
}
