import { useNavigate } from 'react-router-dom'
import { clearAuthToken } from '@/lib/auth'

export function Dashboard() {
  const navigate = useNavigate()

  const handleLogout = () => {
    clearAuthToken()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 justify-between">
            <div className="flex">
              <div className="flex flex-shrink-0 items-center">
                <h1 className="text-xl font-bold text-gray-900">Console</h1>
              </div>
            </div>
            <div className="flex items-center">
              <button
                onClick={handleLogout}
                className="rounded-md bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="rounded-lg bg-white p-6 shadow">
          <h2 className="text-2xl font-semibold text-gray-900">Welcome to the Console</h2>
          <p className="mt-2 text-gray-600">
            This is your admin dashboard. You can manage your application from here.
          </p>

          <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <div className="rounded-lg border border-gray-200 p-4">
              <h3 className="font-semibold text-gray-900">Users</h3>
              <p className="mt-1 text-sm text-gray-600">Manage user accounts</p>
            </div>
            <div className="rounded-lg border border-gray-200 p-4">
              <h3 className="font-semibold text-gray-900">Settings</h3>
              <p className="mt-1 text-sm text-gray-600">Configure your application</p>
            </div>
            <div className="rounded-lg border border-gray-200 p-4">
              <h3 className="font-semibold text-gray-900">Analytics</h3>
              <p className="mt-1 text-sm text-gray-600">View usage statistics</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
