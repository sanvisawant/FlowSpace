import { create } from 'zustand'
import { supabase } from '../lib/supabase'
import axios from 'axios'

interface UserProfile {
  id: string
  email: string
  name?: string
  avatar_url?: string
}

interface AuthState {
  user: UserProfile | null
  token: string | null
  loading: boolean
  initialized: boolean
  signUp: (email: string, password: string) => Promise<void>
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
  init: () => () => void
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080'

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  loading: true,
  initialized: false,

  signUp: async (email, password) => {
    set({ loading: true })
    const { error } = await supabase.auth.signUp({ email, password })
    if (error) {
      set({ loading: false })
      throw error
    }
  },

  signIn: async (email, password) => {
    set({ loading: true })
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) {
      set({ loading: false })
      throw error
    }
  },

  signOut: async () => {
    set({ loading: true })
    const { error } = await supabase.auth.signOut()
    if (error) {
      set({ loading: false })
      throw error
    }
    set({ user: null, token: null, loading: false })
  },

  init: () => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (session) {
        const token = session.access_token
        set({ token })
        
        // Sync user with backend
        axios.get(`${API_URL}/api/auth/me`, {
          headers: { Authorization: `Bearer ${token}` }
        }).then((res) => {
          set({ user: res.data, loading: false, initialized: true })
        }).catch((err) => {
          console.error("Backend auth sync failed:", err)
          set({ loading: false, initialized: true })
        })
      } else {
        set({ user: null, token: null, loading: false, initialized: true })
      }
    })

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (_, session) => {
      if (session) {
        const token = session.access_token
        set({ token })
        try {
          const res = await axios.get(`${API_URL}/api/auth/me`, {
            headers: { Authorization: `Bearer ${token}` }
          })
          set({ user: res.data, loading: false, initialized: true })
        } catch (err) {
          console.error("Backend auth sync failed on change:", err)
          set({ user: { id: session.user.id, email: session.user.email || "" }, loading: false, initialized: true })
        }
      } else {
        set({ user: null, token: null, loading: false, initialized: true })
      }
    })

    return () => {
      subscription.unsubscribe()
    }
  }
}))
