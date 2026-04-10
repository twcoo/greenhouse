import type { User } from "./user"

export interface createAdminPayload {
  username: string
  password: string
  password2: string
}

export interface createAdminResponse {
  expiry: string
  token: string
  user: User
}
