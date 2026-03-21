import { User } from "./user"

export interface authLoginResponse {
  user: User
}

export interface authLoginPayload {
  username: string
  password: string
}
