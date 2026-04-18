<script setup lang="ts">
import { reactive, ref, watch } from "vue"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import type { PlantingLocationPayload } from "@/types/plantingLocation"
import type { APIErrorResponse } from "@/types/api"
import { FieldGroup, Field, FieldLabel, FieldError } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import {
  plantingLocationSchema,
  type PlantingLocationForm,
} from "@/schemas/plantingLocation.schemas"
import { apiToFormErrors, zodToFormErrors } from "@/utils/formErrors"
import { AxiosError } from "axios"
import { IconLoader2 } from "@tabler/icons-vue"

const open = defineModel<boolean>("open")
const { isLoading, isCreateSuccess } = defineProps<{
  isLoading: boolean
  isCreateSuccess: boolean
}>()

const emit = defineEmits<{
  (e: "submit", payload: PlantingLocationPayload, onError: (err: unknown) => void): void
}>()

const formInitialState: PlantingLocationForm = {
  name: "",
  locationType: "POT",
  width: 1,
  height: 1,
  length: undefined,
}

const form = reactive<PlantingLocationForm>({ ...formInitialState })
const errors = ref<Record<string, string>>({})

const handleSubmit = async (): Promise<void> => {
  const result = plantingLocationSchema.safeParse(form)

  if (!result.success) {
    errors.value = zodToFormErrors(result.error)
    return
  }

  emit("submit", result.data, (err: unknown) => {
    const axiosError = err as AxiosError<APIErrorResponse>
    if (axiosError.response?.data) {
      errors.value = apiToFormErrors(axiosError.response.data.message)
    } else {
      errors.value.general = "Something went wrong. Please try again."
    }
  })
}

const resetForm = (): void => {
  Object.assign(form, formInitialState)
  errors.value = {}
}

watch(
  () => isCreateSuccess,
  (success) => {
    if (success) {
      open.value = false
      resetForm()
    }
  },
)

watch(
  () => form.locationType,
  (newType) => {
    if (newType === "GROUND") {
      form.height = undefined
      form.length = 1
    } else {
      form.length = undefined
      form.height = 1
    }
  },
)
</script>

<template>
  <Dialog v-model:open="open">
    <form id="location-form" @submit.prevent="handleSubmit">
      <DialogContent class="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add Planting Location</DialogTitle>
          <DialogDescription>
            Add a new planting location. Fill in the details below.
          </DialogDescription>
        </DialogHeader>
        <FieldGroup>
          <Field>
            <FieldLabel for="name">Name</FieldLabel>
            <Input v-model="form.name" id="name" name="name" />
            <FieldError data-test="nameError" v-if="errors.name">
              {{ errors.name }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel for="locationType">Location Type</FieldLabel>
            <Select id="locationType" v-model="form.locationType">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="NURSERYPOT"> Nursery Pot </SelectItem>
                <SelectItem value="POT"> Pot </SelectItem>
                <SelectItem value="GROUND"> Ground </SelectItem>
              </SelectContent>
            </Select>
            <FieldError data-test="locationTypeError" v-if="errors.locationType">
              {{ errors.locationType }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel for="width">Width (cm)</FieldLabel>
            <Input v-model="form.width" type="number" step="0.01" id="width" name="width" />
            <FieldError data-test="widthError" v-if="errors.width">
              {{ errors.width }}
            </FieldError>
          </Field>
          <Field v-if="form.locationType !== 'GROUND'">
            <FieldLabel for="height">Height (cm)</FieldLabel>
            <Input v-model="form.height" type="number" step="0.01" id="height" name="height" />
            <FieldError data-test="heightError" v-if="errors.height">
              {{ errors.height }}
            </FieldError>
          </Field>
          <Field v-if="form.locationType === 'GROUND'">
            <FieldLabel for="length">Length (m)</FieldLabel>
            <Input v-model="form.length" type="number" step="0.01" id="length" name="length" />
            <FieldError data-test="lengthError" v-if="errors.length">
              {{ errors.length }}
            </FieldError>
          </Field>
        </FieldGroup>
        <DialogFooter>
          <DialogClose as-child>
            <Button variant="outline"> Cancel </Button>
          </DialogClose>
          <Button type="submit" form="location-form">
            <IconLoader2 v-if="isLoading" :size="18" class="animate-spin" />
            {{ isLoading ? "Saving..." : "Save" }}
          </Button>
        </DialogFooter>
        <p
          data-test="general-error"
          v-if="errors.general"
          class="text-sm text-red-500 m-2 text-center"
        >
          {{ errors.general }}
        </p>
      </DialogContent>
    </form>
  </Dialog>
</template>
