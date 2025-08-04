import { UserButton } from '@clerk/nextjs'
import { currentUser } from '@clerk/nextjs/server'
import { redirect } from 'next/navigation'

export default async function Dashboard() {
  const user = await currentUser()

   if (!user) {
    redirect('/sign-in')
  }
  
  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">Welcome to Chronoverse</h1>
          <p className="text-gray-600">Hello, {user?.firstName}!</p>
        </div>
        <UserButton afterSignOutUrl="/" />
      </div>
      
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Your Historical Worlds</h2>
        <p>World selection and 3D experiences will go here...</p>
      </div>
    </div>
  )
}
