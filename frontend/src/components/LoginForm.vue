<script setup lang="ts">
import { reactive, ref } from "vue"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Field, FieldGroup, FieldLabel, FieldError } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "@/stores/authStore"
import { authLoginSchema, type authLoginForm } from "@/schemas/auth.schema"
import { IconLoader2 } from "@tabler/icons-vue"
import { zodToFormErrors } from "@/utils/formErrors"

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()
const form = reactive<authLoginForm>({
  username: "",
  password: "",
})
const errors = ref<Record<string, string>>({})

async function handleSubmit(): Promise<void> {
  errors.value = {}

  const result = authLoginSchema.safeParse(form)

  if (!result.success) {
    errors.value = zodToFormErrors(result.error)
    return
  }

  await authStore.login(result.data)

  if (authStore.isAuthenticated) {
    const redirectTo = route.query?.redirectTo

    router.push(redirectTo || { name: "dashboard" })
  }
}
</script>

<template>
  <div class="flex flex-col gap-6">
    <Card>
      <CardHeader>
        <CardTitle>Login to your account</CardTitle>
        <CardDescription> Enter your username below to login to your account </CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleSubmit">
          <FieldGroup>
            <Field>
              <FieldLabel for="username"> Username </FieldLabel>
              <Input
                v-model="form.username"
                id="username"
                type="text"
                placeholder="jmiller"
                required
              />
              <FieldError data-test="username-error" v-if="errors.username">
                {{ errors.username }}
              </FieldError>
            </Field>
            <Field>
              <div class="flex items-center">
                <FieldLabel for="password"> Password </FieldLabel>
              </div>
              <Input v-model="form.password" id="password" type="password" required />
              <FieldError data-test="password-error" v-if="errors.password">
                {{ errors.password }}
              </FieldError>
            </Field>
            <Field>
              <Button type="submit" :disabled="authStore.loading">
                <IconLoader2 v-if="authStore.loading" :size="18" class="animate-spin" />
                {{ authStore.loading ? "Logging in..." : "Login" }}
              </Button>
            </Field>
          </FieldGroup>
          <p
            data-test="general-error"
            v-if="authStore.error"
            class="text-sm text-red-500 m-2 text-center"
          >
            {{ authStore.error }}
          </p>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
