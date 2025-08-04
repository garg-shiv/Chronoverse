import { SignInButton, SignUpButton, UserButton } from '@clerk/nextjs'
import { currentUser } from '@clerk/nextjs/server'
import Link from 'next/link'

export default async function Home() {
  const user = await currentUser()

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      <nav className="p-6 flex justify-between items-center">
        <h1 className="text-2xl font-bold">Chronoverse</h1>
        <div className="flex items-center gap-4">
          {user ? (
            <>
              <Link href="/dashboard" className="bg-amber-600 px-4 py-2 rounded-lg hover:bg-amber-700">
                Dashboard
              </Link>
              <UserButton afterSignOutUrl="/" />
            </>
          ) : (
            <>
              <SignInButton mode="modal">
                <button className="px-4 py-2 border border-white rounded-lg hover:bg-white hover:text-black">
                  Sign In
                </button>
              </SignInButton>
              <SignUpButton mode="modal">
                <button className="bg-amber-600 px-4 py-2 rounded-lg hover:bg-amber-700">
                  Get Started
                </button>
              </SignUpButton>
            </>
          )}
        </div>
      </nav>

      <div className="flex items-center justify-center min-h-[80vh] text-center">
        <div>
          <h2 className="text-6xl font-bold mb-6">Journey Through History</h2>
          <p className="text-xl mb-8 text-gray-300">Experience immersive conversations with historical figures</p>
          {!user && (
            <SignUpButton mode="modal">
              <button className="bg-amber-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-amber-700">
                Enter the Time Portal
              </button>
            </SignUpButton>
          )}
        </div>
      </div>
    </div>
  )
}
