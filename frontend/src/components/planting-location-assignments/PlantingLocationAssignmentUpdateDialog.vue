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
import DatePicker from "@/components/DatePicker.vue"
import { FieldGroup, Field, FieldLabel, FieldError } from "@/components/ui/field"
import {
  plantingLocationAssignmentSchema,
  type PlantingLocationAssignmentForm,
} from "@/schemas/plantingLocationAssignment.schemas"
import type { PlantingLocationAssignmentPayload } from "@/types/plantingLocationAssignment"
import type { APIErrorResponse } from "@/types/api"
import { apiToFormErrors, zodToFormErrors } from "@/utils/formErrors"
import { AxiosError } from "axios"
import { IconLoader2 } from "@tabler/icons-vue"
import { usePlantingLocations } from "@/composables/usePlantingLocations"

const open = defineModel<boolean>("open")
const { id, assignmentFormInitialState, isLoading, isUpdateSuccess } = defineProps<{
  id: number
  assignmentFormInitialState: PlantingLocationAssignmentForm
  isLoading: boolean
  isUpdateSuccess: boolean
}>()

const emit = defineEmits<{
  (
    e: "submit",
    id: number,
    payload: PlantingLocationAssignmentPayload,
    onError: (err: unknown) => void,
  ): void
}>()

const locationPagination = ref({ pageIndex: 0, pageSize: 100 })
const { locations } = usePlantingLocations(locationPagination)

const form = reactive<PlantingLocationAssignmentForm>({
  ...assignmentFormInitialState,
})
const selectedLocationId = ref<string>(String(assignmentFormInitialState.plantingLocation))
const errors = ref<Record<string, string>>({})

watch(
  () => assignmentFormInitialState,
  (newVal) => {
    Object.assign(form, newVal)
    selectedLocationId.value = String(newVal.plantingLocation)
    errors.value = {}
  },
  { deep: true },
)

const handleSubmit = async (): Promise<void> => {
  const result = plantingLocationAssignmentSchema.safeParse({
    ...form,
    plantingLocation: selectedLocationId.value,
  })

  if (!result.success) {
    errors.value = zodToFormErrors(result.error)
    return
  }

  const payload: PlantingLocationAssignmentPayload = {
    plantingLocation: result.data.plantingLocation,
    startDate: result.data.startDate,
    ...(result.data.endDate ? { endDate: result.data.endDate } : {}),
  }

  emit("submit", id, payload, (err: unknown) => {
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
    errors.value = {}
    Object.assign(form, assignmentFormInitialState)
    selectedLocationId.value = String(assignmentFormInitialState.plantingLocation)
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
    <form id="assignment-update-form" @submit.prevent="handleSubmit">
      <DialogContent class="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Update Location Assignment</DialogTitle>
          <DialogDescription>Update the location assignment details below.</DialogDescription>
        </DialogHeader>
        <FieldGroup>
          <Field>
            <FieldLabel for="location">Location</FieldLabel>
            <Select id="location" v-model="selectedLocationId">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select location" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem
                  v-for="location in locations?.results"
                  :key="location.id"
                  :value="String(location.id)"
                >
                  {{ location.name }}
                </SelectItem>
              </SelectContent>
            </Select>
            <FieldError data-test="plantingLocationError" v-if="errors.plantingLocation">
              {{ errors.plantingLocation }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel>Start Date</FieldLabel>
            <DatePicker v-model="form.startDate" placeholder="Pick a start date" />
            <FieldError data-test="startDateError" v-if="errors.startDate">
              {{ errors.startDate }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel>End Date (optional)</FieldLabel>
            <DatePicker v-model="form.endDate" placeholder="Pick an end date" />
            <FieldError data-test="endDateError" v-if="errors.endDate">
              {{ errors.endDate }}
            </FieldError>
          </Field>
        </FieldGroup>
        <DialogFooter>
          <DialogClose as-child>
            <Button variant="outline">Cancel</Button>
          </DialogClose>
          <Button type="submit" form="assignment-update-form" :disabled="isLoading">
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
