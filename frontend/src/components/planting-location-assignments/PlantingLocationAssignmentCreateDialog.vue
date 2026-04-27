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
const { isLoading, isCreateSuccess } = defineProps<{
  isLoading: boolean
  isCreateSuccess: boolean
}>()

const emit = defineEmits<{
  (e: "submit", payload: PlantingLocationAssignmentPayload, onError: (err: unknown) => void): void
}>()

const locationPagination = ref({ pageIndex: 0, pageSize: 100 })
const { locations } = usePlantingLocations(locationPagination)

const formInitialState: PlantingLocationAssignmentForm = {
  plantingLocation: 0,
  startDate: "",
  endDate: undefined,
}

const form = reactive<PlantingLocationAssignmentForm>({ ...formInitialState })
const selectedLocationId = ref<string>("")
const errors = ref<Record<string, string>>({})

const resetForm = (): void => {
  Object.assign(form, formInitialState)
  selectedLocationId.value = ""
  errors.value = {}
}

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

  emit("submit", payload, (err: unknown) => {
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
    if (success) {
      open.value = false
      resetForm()
    }
  },
)

watch(open, (isOpen) => {
  if (!isOpen) resetForm()
})
</script>

<template>
  <Dialog v-model:open="open">
    <form id="assignment-create-form" @submit.prevent="handleSubmit">
      <DialogContent class="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add Location Assignment</DialogTitle>
          <DialogDescription>
            Assign this planting to a location for the given date range.
          </DialogDescription>
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
          <Button type="submit" form="assignment-create-form" :disabled="isLoading">
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
