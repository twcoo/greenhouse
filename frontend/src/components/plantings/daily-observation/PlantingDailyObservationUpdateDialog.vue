<script setup lang="ts">
import { computed, reactive, ref, useTemplateRef, watch } from "vue"
import { getFileFromEvent } from "@/utils/formData"
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
import { Input } from "@/components/ui/input"
import { FieldGroup, Field, FieldLabel, FieldError } from "@/components/ui/field"
import { Checkbox } from "@/components/ui/checkbox"
import { IconLoader2, IconX } from "@tabler/icons-vue"
import {
  plantingDailyObservationSchema,
  type PlantingDailyObservationForm,
} from "@/schemas/plantingDailyObservation.schemas"
import type { APIErrorResponse } from "@/types/api"
import { apiToFormErrors, zodToFormErrors } from "@/utils/formErrors"
import { AxiosError } from "axios"
import { HEALTH_STATUS_OPTIONS, PEST_PRESSURE_OPTIONS } from "./constants"

const open = defineModel<boolean>("open")
const { id, observationFormInitialState, isLoading, isUpdateSuccess, currentImage } = defineProps<{
  id: number
  observationFormInitialState: PlantingDailyObservationForm
  isLoading: boolean
  isUpdateSuccess: boolean
  currentImage?: string | null
}>()

const emit = defineEmits<{
  (
    e: "submit",
    id: number,
    payload: PlantingDailyObservationForm,
    onError: (err: unknown) => void,
  ): void
}>()

const form = reactive<PlantingDailyObservationForm>({ ...observationFormInitialState })
const errors = ref<Record<string, string>>({})
const fileInputRef = useTemplateRef<HTMLInputElement>("fileInputRef")

watch(
  () => observationFormInitialState,
  (newVal) => {
    Object.assign(form, newVal)
    errors.value = {}
  },
  { deep: true },
)

const imageLabel = computed(() => {
  if (form.image instanceof File) return form.image.name
  if (currentImage && form.image !== null) return currentImage.split("/").pop()
  return "No image"
})

const showRemoveImageButton = computed(
  () =>
    (!!currentImage && form.image !== null && !(form.image instanceof File)) ||
    form.image instanceof File,
)

const triggerFileInput = (): void => {
  fileInputRef.value?.click()
}

const handleImageChange = (event: Event): void => {
  form.image = getFileFromEvent(event)
}

const handleRemoveImage = (): void => {
  form.image = currentImage ? null : undefined
  if (fileInputRef.value) fileInputRef.value.value = ""
}

const handleSubmit = (): void => {
  const result = plantingDailyObservationSchema.safeParse(form)

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

watch(open, (isOpen) => {
  if (!isOpen) {
    if (fileInputRef.value) fileInputRef.value.value = ""
  } else {
    errors.value = {}
    Object.assign(form, observationFormInitialState)
  }
})

watch(
  () => isUpdateSuccess,
  (success) => {
    if (success) open.value = false
  },
)
</script>

<template>
  <Dialog v-model:open="open">
    <form id="observation-update-form" @submit.prevent="handleSubmit">
      <DialogContent class="sm:max-w-lg max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Edit Observation</DialogTitle>
          <DialogDescription>Update this daily observation.</DialogDescription>
        </DialogHeader>

        <FieldGroup>
          <!-- Health -->
          <p class="text-xs font-semibold uppercase text-muted-foreground tracking-wide">Health</p>
          <Field>
            <FieldLabel for="healthStatus">Health Status</FieldLabel>
            <Select id="healthStatus" v-model="form.healthStatus">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select health status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem
                  v-for="opt in HEALTH_STATUS_OPTIONS"
                  :key="opt.value"
                  :value="opt.value"
                >
                  {{ opt.label }}
                </SelectItem>
              </SelectContent>
            </Select>
            <FieldError data-test="healthStatusError" v-if="errors.healthStatus">
              {{ errors.healthStatus }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel for="pestPressure">Pest Pressure</FieldLabel>
            <Select id="pestPressure" v-model="form.pestPressure">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select pest pressure" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem
                  v-for="opt in PEST_PRESSURE_OPTIONS"
                  :key="opt.value"
                  :value="opt.value"
                >
                  {{ opt.label }}
                </SelectItem>
              </SelectContent>
            </Select>
            <FieldError data-test="pestPressureError" v-if="errors.pestPressure">
              {{ errors.pestPressure }}
            </FieldError>
          </Field>
          <Field>
            <div class="flex items-center gap-2">
              <Checkbox id="diseaseSymptoms" v-model="form.diseaseSymptoms" />
              <FieldLabel for="diseaseSymptoms" class="mb-0">Disease symptoms present</FieldLabel>
            </div>
          </Field>
          <Field>
            <div class="flex items-center gap-2">
              <Checkbox id="watered" v-model="form.watered" />
              <FieldLabel for="watered" class="mb-0">Watered</FieldLabel>
            </div>
          </Field>

          <!-- Growth -->
          <p class="text-xs font-semibold uppercase text-muted-foreground tracking-wide mt-2">
            Growth
          </p>
          <div class="grid grid-cols-2 gap-3">
            <Field>
              <FieldLabel for="heightCm">Height (cm)</FieldLabel>
              <Input id="heightCm" v-model="form.heightCm" type="number" step="0.01" min="0" />
              <FieldError data-test="heightCmError" v-if="errors.heightCm">
                {{ errors.heightCm }}
              </FieldError>
            </Field>
            <Field>
              <FieldLabel for="leafCount">Leaf Count</FieldLabel>
              <Input id="leafCount" v-model="form.leafCount" type="number" min="0" />
              <FieldError data-test="leafCountError" v-if="errors.leafCount">
                {{ errors.leafCount }}
              </FieldError>
            </Field>
          </div>

          <!-- Environment -->
          <p class="text-xs font-semibold uppercase text-muted-foreground tracking-wide mt-2">
            Environment
          </p>
          <div class="grid grid-cols-3 gap-3">
            <Field>
              <FieldLabel for="temperatureC">Temp (°C)</FieldLabel>
              <Input id="temperatureC" v-model="form.temperatureC" type="number" step="0.1" />
              <FieldError data-test="temperatureCError" v-if="errors.temperatureC">
                {{ errors.temperatureC }}
              </FieldError>
            </Field>
            <Field>
              <FieldLabel for="humidityPercent">Humidity (%)</FieldLabel>
              <Input
                id="humidityPercent"
                v-model="form.humidityPercent"
                type="number"
                step="0.01"
                min="0"
                max="100"
              />
              <FieldError data-test="humidityPercentError" v-if="errors.humidityPercent">
                {{ errors.humidityPercent }}
              </FieldError>
            </Field>
            <Field>
              <FieldLabel for="lightHours">Light (hrs)</FieldLabel>
              <Input id="lightHours" v-model="form.lightHours" type="number" step="0.01" min="0" />
              <FieldError data-test="lightHoursError" v-if="errors.lightHours">
                {{ errors.lightHours }}
              </FieldError>
            </Field>
          </div>

          <!-- Soil -->
          <p class="text-xs font-semibold uppercase text-muted-foreground tracking-wide mt-2">
            Soil
          </p>
          <div class="grid grid-cols-3 gap-3">
            <Field>
              <FieldLabel for="soilMoisturePercent">Moisture (%)</FieldLabel>
              <Input
                id="soilMoisturePercent"
                v-model="form.soilMoisturePercent"
                type="number"
                step="0.01"
                min="0"
                max="100"
              />
              <FieldError data-test="soilMoisturePercentError" v-if="errors.soilMoisturePercent">
                {{ errors.soilMoisturePercent }}
              </FieldError>
            </Field>
            <Field>
              <FieldLabel for="soilPh">pH</FieldLabel>
              <Input id="soilPh" v-model="form.soilPh" type="number" step="0.1" min="0" max="14" />
              <FieldError data-test="soilPhError" v-if="errors.soilPh">
                {{ errors.soilPh }}
              </FieldError>
            </Field>
            <Field>
              <FieldLabel for="ecMsCm">EC (mS/cm)</FieldLabel>
              <Input id="ecMsCm" v-model="form.ecMsCm" type="number" step="0.01" min="0" />
              <FieldError data-test="ecMsCmError" v-if="errors.ecMsCm">
                {{ errors.ecMsCm }}
              </FieldError>
            </Field>
          </div>

          <!-- Notes & Image -->
          <p class="text-xs font-semibold uppercase text-muted-foreground tracking-wide mt-2">
            Notes & Image
          </p>
          <Field>
            <FieldLabel for="notes">Notes</FieldLabel>
            <textarea
              id="notes"
              v-model="form.notes"
              class="border-input placeholder:text-muted-foreground focus-visible:ring-ring flex min-h-[80px] w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 disabled:cursor-not-allowed disabled:opacity-50"
              placeholder="Optional notes about this observation..."
            />
            <FieldError data-test="notesError" v-if="errors.notes">
              {{ errors.notes }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel>Image (optional)</FieldLabel>
            <div
              class="flex items-center border rounded-md overflow-hidden cursor-pointer"
              data-test="image-input-area"
              @click="triggerFileInput"
            >
              <span class="flex-1 px-3 py-2 text-sm truncate text-muted-foreground">
                {{ imageLabel }}
              </span>
              <button
                v-if="showRemoveImageButton"
                type="button"
                data-test="remove-image-button"
                class="px-2 py-2 hover:bg-muted"
                @click.stop="handleRemoveImage"
              >
                <IconX :size="14" />
              </button>
            </div>
            <input
              ref="fileInputRef"
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleImageChange"
            />
            <p v-if="form.image === null" data-test="image-removal-hint" class="text-xs text-muted-foreground">
              Image will be removed on save. Click above to add a new one.
            </p>
            <FieldError data-test="imageError" v-if="errors.image">
              {{ errors.image }}
            </FieldError>
          </Field>
        </FieldGroup>

        <DialogFooter>
          <DialogClose as-child>
            <Button variant="outline" type="button">Cancel</Button>
          </DialogClose>
          <Button type="submit" form="observation-update-form" :disabled="isLoading">
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
