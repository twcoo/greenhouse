import { User } from "./user"

export interface authLoginData {
  user: User
}

export interface authLoginPayload {
  username: string
  password: string
}
