import { useAuthStore } from '../store/authStore'
import { LogOut, User, Mail, Play, AlertCircle } from 'lucide-react'

export default function Dashboard() {
  const { user, signOut, loading } = useAuthStore()

  const handleLogout = async () => {
    try {
      await signOut()
    } catch (err) {
      console.error('Failed to log out:', err)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col">
      {/* Navbar */}
      <header className="border-b border-slate-900 bg-slate-900/20 backdrop-blur-md sticky top-0 z-50 px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-indigo-500 animate-ping"></div>
          <span className="font-extrabold tracking-tight bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent text-xl">
            FlowSpace
          </span>
        </div>

        <button
          onClick={handleLogout}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 border border-slate-800 hover:bg-slate-900 rounded-xl text-xs font-semibold tracking-wider text-slate-300 transition duration-200 cursor-pointer"
        >
          <LogOut className="w-3.5 h-3.5" />
          <span>Logout</span>
        </button>
      </header>

      {/* Content */}
      <main className="flex-1 max-w-4xl w-full mx-auto p-6 md:p-12 space-y-8">
        {/* Profile Card */}
        <section className="bg-slate-900/20 border border-slate-900 p-8 rounded-3xl space-y-4">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-slate-400">User Profile</h2>
          <div className="flex flex-col md:flex-row md:items-center gap-6">
            <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
              <User className="w-8 h-8" />
            </div>
            <div className="space-y-1">
              <p className="text-xl font-bold">{user?.name || user?.email?.split('@')[0] || 'User'}</p>
              <div className="flex items-center gap-1.5 text-xs text-slate-400">
                <Mail className="w-3.5 h-3.5" />
                <span>{user?.email}</span>
              </div>
            </div>
          </div>
        </section>

        {/* Empty State sessions */}
        <section className="bg-slate-900/10 border border-dashed border-slate-900 p-12 rounded-3xl text-center space-y-4">
          <div className="flex justify-center">
            <div className="p-4 bg-slate-900/50 rounded-2xl text-slate-400">
              <AlertCircle className="w-8 h-8" />
            </div>
          </div>
          <div className="space-y-1">
            <h3 className="text-lg font-semibold text-slate-300">No sessions logged yet</h3>
            <p className="text-slate-500 text-sm max-w-xs mx-auto">
              Your focus session logs, stats, and calendar records will appear here once you start.
            </p>
          </div>
          <div className="pt-2">
            <button className="px-5 py-2.5 bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/20 hover:border-indigo-500/35 rounded-xl text-xs font-semibold text-indigo-400 flex items-center justify-center gap-2 mx-auto cursor-pointer transition duration-200">
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>Start Session (Coming Soon)</span>
            </button>
          </div>
        </section>
      </main>
    </div>
  )
}
