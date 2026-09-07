<script setup lang="ts">
import { computed, reactive, ref, watch } from "vue"
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
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { IconLoader2 } from "@tabler/icons-vue"
import {
  plantingDailyObservationSchema,
  type PlantingDailyObservationForm,
} from "@/schemas/plantingDailyObservation.schemas"
import type { APIErrorResponse } from "@/types/api"
import type { Planting } from "@/types/planting"
import { apiToFormErrors, zodToFormErrors } from "@/utils/formErrors"
import { AxiosError } from "axios"
import {
  FERTILIZER_TYPE_OPTIONS,
  HEALTH_STATUS_OPTIONS,
  PEST_PRESSURE_OPTIONS,
  WATERING_EVENT_OPTIONS,
} from "./constants"
import DatePicker from "@/components/DatePicker.vue"
import { today, getLocalTimeZone } from "@internationalized/date"

const open = defineModel<boolean>("open")
const { isLoading, isCreateSuccess, selectedPlantings } = defineProps<{
  isLoading: boolean
  isCreateSuccess: boolean
  selectedPlantings: Planting[]
}>()

const emit = defineEmits<{
  (e: "submit", payload: PlantingDailyObservationForm, onError: (err: unknown) => void): void
}>()

const plantingSummary = computed(() => {
  const names = selectedPlantings.map((p) => `${p.cropName} (${p.varietyName})`)
  return names.join(", ")
})

const formInitialState: PlantingDailyObservationForm = {
  observationDate: today(getLocalTimeZone()).toString(),
  healthStatus: "GOOD",
  pestPressure: "NONE",
  diseaseSymptoms: false,
  wateringEvent: undefined,
  fertilizerType: "NONE",
  fertilizerDetail: "",
  pruned: false,
  pruningDetail: "",
  notes: "",
}

const form = reactive<PlantingDailyObservationForm>({ ...formInitialState })
const errors = ref<Record<string, string>>({})
const resetForm = (): void => {
  Object.assign(form, formInitialState)
  errors.value = {}
}

const handleSubmit = (): void => {
  const result = plantingDailyObservationSchema.safeParse(form)
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

watch(
  () => isCreateSuccess,
  (success) => {
    if (success) open.value = false
  },
)

watch(open, (isOpen) => {
  if (isOpen) {
    resetForm()
  }
})
</script>

<template>
  <Dialog v-model:open="open">
    <form id="bulk-observation-create-form" @submit.prevent="handleSubmit">
      <DialogContent class="sm:max-w-lg max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Log Observation for {{ selectedPlantings.length }} Plantings</DialogTitle>
          <DialogDescription>
            Record the same daily observation for all selected plantings.
          </DialogDescription>
        </DialogHeader>

        <p class="text-sm text-muted-foreground -mt-2">
          <span class="font-medium">Selected:</span> {{ plantingSummary }}
        </p>

        <FieldGroup>
          <!-- Date -->
          <Field>
            <FieldLabel for="observationDate">Observation Date</FieldLabel>
            <DatePicker id="observationDate" v-model="form.observationDate" />
            <FieldError data-test="observationDateError" v-if="errors.observationDate">
              {{ errors.observationDate }}
            </FieldError>
          </Field>

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

          <!-- Watering -->
          <p class="text-xs font-semibold uppercase text-muted-foreground tracking-wide mt-2">
            Watering
          </p>
          <Field>
            <FieldLabel for="wateringEvent">Watering Event</FieldLabel>
            <Select id="wateringEvent" v-model="form.wateringEvent">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select watering event" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem
                  v-for="opt in WATERING_EVENT_OPTIONS"
                  :key="opt.value"
                  :value="opt.value"
                >
                  {{ opt.label }}
                </SelectItem>
              </SelectContent>
            </Select>
            <FieldError data-test="wateringEventError" v-if="errors.wateringEvent">
              {{ errors.wateringEvent }}
            </FieldError>
          </Field>

          <!-- Pruning -->
          <p class="text-xs font-semibold uppercase text-muted-foreground tracking-wide mt-2">
            Pruning
          </p>
          <Field>
            <div class="flex items-center gap-2">
              <Checkbox id="pruned" v-model="form.pruned" />
              <FieldLabel for="pruned" class="mb-0">Pruned</FieldLabel>
            </div>
          </Field>
          <Field v-if="form.pruned">
            <FieldLabel for="pruningDetail">Pruning Detail</FieldLabel>
            <Input
              id="pruningDetail"
              v-model="form.pruningDetail"
              placeholder="e.g. removed lower leaves, topped the plant"
            />
            <FieldError data-test="pruningDetailError" v-if="errors.pruningDetail">
              {{ errors.pruningDetail }}
            </FieldError>
          </Field>

          <!-- Fertilization -->
          <p class="text-xs font-semibold uppercase text-muted-foreground tracking-wide mt-2">
            Fertilization
          </p>
          <Field>
            <FieldLabel for="fertilizerType">Fertilizer Type</FieldLabel>
            <Select id="fertilizerType" v-model="form.fertilizerType">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select fertilizer type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem
                  v-for="opt in FERTILIZER_TYPE_OPTIONS"
                  :key="opt.value"
                  :value="opt.value"
                >
                  {{ opt.label }}
                </SelectItem>
              </SelectContent>
            </Select>
            <FieldError data-test="fertilizerTypeError" v-if="errors.fertilizerType">
              {{ errors.fertilizerType }}
            </FieldError>
          </Field>
          <Field v-if="form.fertilizerType !== 'NONE'">
            <FieldLabel for="fertilizerDetail">Fertilizer Detail</FieldLabel>
            <Input
              id="fertilizerDetail"
              v-model="form.fertilizerDetail"
              placeholder="e.g. fermented swamp fertilizer"
            />
            <FieldError data-test="fertilizerDetailError" v-if="errors.fertilizerDetail">
              {{ errors.fertilizerDetail }}
            </FieldError>
          </Field>

          <!-- Notes -->
          <p class="text-xs font-semibold uppercase text-muted-foreground tracking-wide mt-2">
            Notes
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
        </FieldGroup>

        <DialogFooter>
          <DialogClose as-child>
            <Button variant="outline" type="button">Cancel</Button>
          </DialogClose>
          <Button type="submit" form="bulk-observation-create-form" :disabled="isLoading">
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
