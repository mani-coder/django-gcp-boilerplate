import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from 'urql'
import { LOGIN_MUTATION } from '@/graphql/mutations'
import { setAuthToken } from '@/lib/auth'

export function AuthCallback() {
  const navigate = useNavigate()
  const [, loginMutation] = useMutation(LOGIN_MUTATION)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const handleCallback = async () => {
      const params = new URLSearchParams(window.location.search)
      const code = params.get('code')

      if (!code) {
        setError('No authorization code found')
        return
      }

      try {
        const result = await loginMutation({ code })

        if (result.error) {
          setError(result.error.message)
          return
        }

        const responseCode = result.data?.login?.responseCode
        const token = result.data?.login?.token

        // Check if login was successful
        if (responseCode === 'LOGIN_SUCCESS' && token) {
          setAuthToken(token)
          navigate('/dashboard')
        } else if (responseCode === 'INVALID_CODE') {
          setError('Authentication failed: Invalid authorization code. Please try again.')
        } else {
          setError(`Login failed: ${responseCode || 'Unknown error'}`)
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred during login')
      }
    }

    handleCallback()
  }, [loginMutation, navigate])

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <h1 className="text-2xl font-semibold text-red-600">Authentication Error</h1>
          <p className="mt-2 text-gray-600">{error}</p>
          <button
            onClick={() => navigate('/login')}
            className="mt-4 rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="text-center">
        <h1 className="text-2xl font-semibold text-gray-900">Completing login...</h1>
        <p className="mt-2 text-gray-600">Please wait while we authenticate you.</p>
      </div>
    </div>
  )
}
