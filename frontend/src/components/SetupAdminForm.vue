<script setup lang="ts">
import { reactive, ref } from "vue"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Field, FieldDescription, FieldGroup, FieldLabel, FieldError } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { useSetup } from "@/composables/useSetup"
import { setupAdminSchema, type setupAdminForm } from "@/schemas/setup.schema"
import { apiToFormErrors, zodToFormErrors } from "@/utils/formErrors"
import { AxiosError } from "axios"
import type { APIErrorResponse } from "@/types/api"
import { IconLoader2, IconEye, IconEyeOff } from "@tabler/icons-vue"
import { useRouter } from "vue-router"
import { useSetupStore } from "@/stores/setupStore"

const setupStore = useSetupStore()
const router = useRouter()
const { setupAdmin, loading } = useSetup()

const form = reactive<setupAdminForm>({
  username: "",
  password: "",
  password2: "",
})

const errors = ref<Record<string, string>>({})
const showPassword = ref(false)
const showPassword2 = ref(false)

async function submit() {
  errors.value = {}

  const result = setupAdminSchema.safeParse(form)

  if (!result.success) {
    errors.value = zodToFormErrors(result.error)
    return
  }

  try {
    await setupAdmin(result.data)
    setupStore.setupRequired = false
    router.push({ name: "dashboard" })
  } catch (err) {
    const axiosError = err as AxiosError<APIErrorResponse>

    if (axiosError.response?.data) {
      const apiErrors = axiosError.response.data.message
      errors.value = apiToFormErrors(apiErrors)
    } else {
      errors.value.general = "Something went wrong. Please try again."
    }
  }
}
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>Create admin account</CardTitle>
      <CardDescription>
        Create the administrator account to complete the application setup.
      </CardDescription>
    </CardHeader>
    <CardContent>
      <form @submit.prevent="submit">
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
            <FieldDescription>
              Choose a unique username. It may contain letters, numbers, underscores, or dots.
            </FieldDescription>
            <FieldError data-test="usernameError" v-if="errors.username">
              {{ errors.username }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel for="password"> Password </FieldLabel>
            <div class="relative">
              <Input
                v-model="form.password"
                id="password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="pr-9"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 flex items-center px-3 text-muted-foreground hover:text-foreground"
                @click="showPassword = !showPassword"
                :aria-label="showPassword ? 'Hide password' : 'Show password'"
              >
                <IconEyeOff v-if="showPassword" :size="16" />
                <IconEye v-else :size="16" />
              </button>
            </div>
            <FieldDescription>Must be at least 8 characters long.</FieldDescription>
            <FieldError data-test="passwordError" v-if="errors.password">
              {{ errors.password }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel for="password2"> Confirm Password </FieldLabel>
            <div class="relative">
              <Input
                v-model="form.password2"
                id="password2"
                :type="showPassword2 ? 'text' : 'password'"
                required
                class="pr-9"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 flex items-center px-3 text-muted-foreground hover:text-foreground"
                @click="showPassword2 = !showPassword2"
                :aria-label="showPassword2 ? 'Hide password' : 'Show password'"
              >
                <IconEyeOff v-if="showPassword2" :size="16" />
                <IconEye v-else :size="16" />
              </button>
            </div>

            <FieldDescription>Please confirm your password.</FieldDescription>
            <FieldError data-test="password2Error" v-if="errors.password2">
              {{ errors.password2 }}
            </FieldError>
          </Field>
          <FieldGroup>
            <Field>
              <Button type="submit" :disabled="loading">
                <IconLoader2 v-if="loading" :size="18" class="animate-spin" />
                {{ loading ? "Creating..." : "Create Account" }}
              </Button>
            </Field>
          </FieldGroup>
        </FieldGroup>
        <p
          data-test="general-error"
          v-if="errors.general"
          class="text-sm text-red-500 m-2 text-center"
        >
          {{ errors.general }}
        </p>
      </form>
    </CardContent>
  </Card>
</template>
