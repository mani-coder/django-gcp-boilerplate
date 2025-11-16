import { useEffect } from 'react'
import { redirectToLogin } from '@/lib/auth'

export function Login() {
  useEffect(() => {
    // Automatically redirect to WorkOS login
    redirectToLogin()
  }, [])

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="text-center">
        <h1 className="text-2xl font-semibold text-gray-900">Redirecting to login...</h1>
        <p className="mt-2 text-gray-600">If you are not redirected automatically, please wait.</p>
      </div>
    </div>
  )
}
