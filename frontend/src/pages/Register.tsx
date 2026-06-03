import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { Sparkles, Mail, Lock, CheckCircle, ArrowRight, Loader2, AlertCircle, Check } from 'lucide-react'
import { verifyEmail } from '../api/auth'

export default function Register() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [errorMsg, setErrorMsg] = useState('')
  const [success, setSuccess] = useState(false)
  const [emailStatus, setEmailStatus] = useState<'idle' | 'checking' | 'valid' | 'invalid'>('idle')
  const [emailFeedback, setEmailFeedback] = useState<string | null>(null)
  const [emailSuggestion, setEmailSuggestion] = useState<string | null>(null)
  const { signUp, loading } = useAuthStore()

  const validateEmail = (emailStr: string) => {
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    return re.test(emailStr)
  }

  const handleEmailCheck = async (emailToCheck: string) => {
    const trimmed = emailToCheck.trim()
    if (!trimmed) {
      setEmailStatus('idle')
      setEmailFeedback(null)
      setEmailSuggestion(null)
      return
    }

    if (!validateEmail(trimmed)) {
      setEmailStatus('invalid')
      setEmailFeedback('Please enter a valid email address.')
      setEmailSuggestion(null)
      return
    }

    setEmailStatus('checking')
    setEmailFeedback(null)
    setEmailSuggestion(null)

    try {
      const res = await verifyEmail(trimmed)
      const isMailboxValid = res.is_valid && (res.is_smtp_valid || res.deliverability === 'DELIVERABLE') && res.deliverability !== 'UNDELIVERABLE'
      
      if (isMailboxValid) {
        setEmailStatus('valid')
        setEmailFeedback(null)
        if (res.autocorrect) {
          setEmailSuggestion(res.autocorrect)
        }
      } else {
        setEmailStatus('invalid')
        setEmailFeedback(res.message || 'This email address does not have an active mailbox.')
        if (res.autocorrect) {
          setEmailSuggestion(res.autocorrect)
        }
      }
    } catch (err: any) {
      console.error('Email verification error:', err)
      // Fallback on network/server errors so users are not blocked
      setEmailStatus('valid')
      setEmailFeedback(null)
    }
  }

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrorMsg('')

    if (emailStatus === 'invalid') {
      setErrorMsg(emailFeedback || 'Please enter a valid email address.')
      return
    }

    if (emailStatus === 'checking') {
      setErrorMsg('Verifying email address, please wait...')
      return
    }

    const trimmedEmail = email.trim()

    // If verification hasn't run yet (e.g. keypress submission without blurring)
    if (emailStatus === 'idle') {
      if (!validateEmail(trimmedEmail)) {
        setErrorMsg('Please enter a valid email address.')
        return
      }

      setEmailStatus('checking')
      try {
        const res = await verifyEmail(trimmedEmail)
        const isMailboxValid = res.is_valid && (res.is_smtp_valid || res.deliverability === 'DELIVERABLE') && res.deliverability !== 'UNDELIVERABLE'
        
        if (!isMailboxValid) {
          setEmailStatus('invalid')
          setEmailFeedback(res.message || 'This email address does not have an active mailbox.')
          setErrorMsg(res.message || 'This email address does not have an active mailbox.')
          if (res.autocorrect) {
            setEmailSuggestion(res.autocorrect)
          }
          return
        }
        setEmailStatus('valid')
      } catch (err) {
        console.error('Email verification error on submit:', err)
        // Fallback to bypass block on error
      }
    }

    try {
      await signUp(trimmedEmail, password)
      setSuccess(true)
    } catch (err: any) {
      setErrorMsg(err.message || 'An error occurred during registration.')
    }
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-radial from-slate-900 via-slate-950 to-black text-white p-6">
      <div className="max-w-md w-full space-y-6 bg-slate-900/40 backdrop-blur-xl border border-slate-800 p-8 rounded-3xl shadow-2xl">
        <div className="flex flex-col items-center text-center space-y-2">
          <div className="p-3 bg-indigo-500/10 rounded-2xl border border-indigo-500/20 text-indigo-400">
            <Sparkles className="h-8 w-8" />
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            Create Account
          </h1>
          <p className="text-slate-400 text-sm">
            Get started with FlowSpace today
          </p>
        </div>

        {success ? (
          <div className="p-5 bg-emerald-500/10 border border-emerald-500/30 rounded-2xl space-y-3 text-center">
            <div className="flex justify-center text-emerald-400">
              <CheckCircle className="w-12 h-12 animate-bounce" />
            </div>
            <h3 className="text-lg font-semibold text-emerald-300">Check Your Email</h3>
            <p className="text-slate-300 text-xs leading-relaxed">
              We have sent a verification link to <span className="font-semibold text-white">{email}</span>. 
              Please click the link in the email to verify your account and sign in.
            </p>
          </div>
        ) : (
          <form onSubmit={handleRegister} className="space-y-4">
            {errorMsg && (
              <div className="p-3 bg-rose-500/10 border border-rose-500/20 rounded-xl text-rose-400 text-xs">
                {errorMsg}
              </div>
            )}

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Email Address</label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-500">
                  <Mail className="h-4 w-4" />
                </span>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => {
                    setEmail(e.target.value)
                    setEmailStatus('idle')
                    setEmailFeedback(null)
                    setEmailSuggestion(null)
                  }}
                  onBlur={() => handleEmailCheck(email)}
                  className={`w-full pl-10 pr-10 py-3 bg-slate-950/60 border rounded-xl focus:outline-none text-sm text-slate-200 transition-all duration-200 ${
                    emailStatus === 'checking'
                      ? 'border-indigo-500/40 focus:border-indigo-500'
                      : emailStatus === 'valid'
                      ? 'border-emerald-500/40 focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/20'
                      : emailStatus === 'invalid'
                      ? 'border-rose-500/40 focus:border-rose-500/60 focus:ring-1 focus:ring-rose-500/20'
                      : 'border-slate-800 focus:border-indigo-500'
                  }`}
                  placeholder="name@domain.com"
                />
                {emailStatus === 'checking' && (
                  <span className="absolute inset-y-0 right-0 flex items-center pr-3">
                    <Loader2 className="h-4 w-4 text-indigo-400 animate-spin" />
                  </span>
                )}
                {emailStatus === 'valid' && (
                  <span className="absolute inset-y-0 right-0 flex items-center pr-3 animate-in fade-in zoom-in-75 duration-200">
                    <Check className="h-4 w-4 text-emerald-400" />
                  </span>
                )}
                {emailStatus === 'invalid' && (
                  <span className="absolute inset-y-0 right-0 flex items-center pr-3 animate-in fade-in zoom-in-75 duration-200">
                    <AlertCircle className="h-4 w-4 text-rose-400" />
                  </span>
                )}
              </div>
              {emailStatus === 'invalid' && emailFeedback && (
                <p className="text-rose-400 text-xs mt-1.5 flex items-center gap-1.5 animate-in slide-in-from-top-1 duration-200">
                  <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                  <span>{emailFeedback}</span>
                </p>
              )}
              {emailSuggestion && (
                <div className="mt-2 p-2.5 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-xs flex items-center justify-between gap-3 animate-in slide-in-from-top-2 duration-300">
                  <span className="text-slate-300">
                    Did you mean <span className="font-semibold text-indigo-300">{emailSuggestion}</span>?
                  </span>
                  <button
                    type="button"
                    onClick={() => {
                      setEmail(emailSuggestion)
                      setEmailSuggestion(null)
                      handleEmailCheck(emailSuggestion)
                    }}
                    className="text-indigo-400 hover:text-indigo-300 font-semibold px-2 py-1 bg-indigo-500/10 hover:bg-indigo-500/20 rounded-lg transition-all cursor-pointer border border-transparent"
                  >
                    Use Suggestion
                  </button>
                </div>
              )}
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Password</label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-500">
                  <Lock className="h-4 w-4" />
                </span>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 bg-slate-950/60 border border-slate-800 rounded-xl focus:outline-none focus:border-indigo-500 text-sm text-slate-200"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 mt-2 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 disabled:opacity-50 text-white font-semibold rounded-xl text-sm transition-all duration-200 shadow-lg shadow-indigo-500/10 flex items-center justify-center gap-2 cursor-pointer"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              ) : (
                <>
                  <span>Sign Up</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>
        )}

        <div className="text-center pt-2">
          <p className="text-xs text-slate-500">
            Already have an account?{' '}
            <Link to="/login" className="text-indigo-400 hover:underline font-medium">
              Sign In
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
