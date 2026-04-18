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
import { FieldGroup, Field, FieldLabel, FieldError } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import {
  plantingLocationSchema,
  type PlantingLocationForm,
} from "@/schemas/plantingLocation.schemas"
import type { PlantingLocationPayload } from "@/types/plantingLocation"
import { apiToFormErrors, zodToFormErrors } from "@/utils/formErrors"
import { AxiosError } from "axios"
import type { APIErrorResponse } from "@/types/api"
import { IconLoader2 } from "@tabler/icons-vue"

const open = defineModel<boolean>("open")
const { id, locationFormInitialState, isLoading, isUpdateSuccess } = defineProps<{
  id: number
  locationFormInitialState: PlantingLocationForm
  isLoading: boolean
  isUpdateSuccess: boolean
}>()

const emit = defineEmits<{
  (e: "submit", id: number, payload: PlantingLocationPayload, onError: (err: unknown) => void): void
}>()

const form = reactive<PlantingLocationForm>({ ...locationFormInitialState })
const errors = ref<Record<string, string>>({})

// Watch for location to update change
watch(
  () => locationFormInitialState,
  (newVal) => {
    Object.assign(form, newVal)
    errors.value = {}
  },
  { deep: true },
)

const handleSubmit = async (): Promise<void> => {
  const result = plantingLocationSchema.safeParse(form)

  if (!result.success) {
    errors.value = zodToFormErrors(result.error)
    return
  }

  emit("submit", id, result.data, (err: unknown) => {
    const axiosError = err as AxiosError<APIErrorResponse>
    if (axiosError.response?.data) {
      errors.value = apiToFormErrors(axiosError.response.data.message)
    } else {
      errors.value.general = "Something went wrong. Please try again."
    }
  })
}

// Automatically reset the form if it's closed and opened again
watch(open, (isOpen) => {
  if (!isOpen) {
    errors.value = {}
    Object.assign(form, locationFormInitialState)
  }
})

// Automatically close on success
watch(
  () => isUpdateSuccess,
  (success) => {
    if (success) open.value = false
  },
)

watch(
  () => form.locationType,
  (newType) => {
    if (newType === "GROUND") {
      form.height = undefined
      if (form.length === undefined) form.length = 1
    } else {
      form.length = undefined
      if (form.height === undefined) form.height = 1
    }
  },
)
</script>

<template>
  <Dialog v-model:open="open">
    <form id="update-location-form" @submit.prevent="handleSubmit">
      <DialogContent class="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Update Planting Location</DialogTitle>
          <DialogDescription> Update the details of your planting location. </DialogDescription>
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
          <Button type="submit" form="update-location-form" :disabled="isLoading">
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
