<script setup lang="ts">
import { reactive, ref } from "vue"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Field, FieldDescription, FieldGroup, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { useSetup } from "@/composables/useSetup"
import { setupAdminSchema, type setupAdminForm } from "@/schemas/setup.schema"
import { apiToFormErrors, zodToFormErrors } from "@/utils/formErrors"
import { AxiosError } from "axios"
import { APIErrorResponse } from "@/types/api"
import { IconLoader2 } from "@tabler/icons-vue"
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

            <p data-test="username-error" v-if="errors.username" class="text-sm text-red-500">
              {{ errors.username }}
            </p>
          </Field>
          <Field>
            <FieldLabel for="password"> Password </FieldLabel>
            <Input v-model="form.password" id="password" type="password" required />
            <FieldDescription>Must be at least 8 characters long.</FieldDescription>

            <p data-test="password-error" v-if="errors.password" class="text-sm text-red-500">
              {{ errors.password }}
            </p>
          </Field>
          <Field>
            <FieldLabel for="password2"> Confirm Password </FieldLabel>
            <Input v-model="form.password2" id="password2" type="password" required />

            <FieldDescription>Please confirm your password.</FieldDescription>

            <p data-test="password2-error" v-if="errors.password2" class="text-sm text-red-500">
              {{ errors.password2 }}
            </p>
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
        <p data-test="general-error" v-if="errors.general" class="text-sm text-red-500 mb-2">
          {{ errors.general }}
        </p>
      </form>
    </CardContent>
  </Card>
</template>
