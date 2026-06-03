import { client } from './client'

export interface VerifyEmailResponse {
  is_valid: boolean
  is_smtp_valid: boolean
  deliverability: string
  autocorrect: string
  message: string
}

export const verifyEmail = async (email: string): Promise<VerifyEmailResponse> => {
  const response = await client.post<VerifyEmailResponse>('/api/auth/verify-email', { email })
  return response.data
}
