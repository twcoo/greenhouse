<script setup lang="ts">
import { reactive, ref, watch } from "vue"
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
import { FieldGroup, Field, FieldLabel, FieldError } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { IconLoader2 } from "@tabler/icons-vue"
import {
  plantingLocationStatusSchema,
  MANUAL_STATUS_CHOICES,
  type PlantingLocationStatusForm,
} from "@/schemas/plantingLocationStatus.schemas"
import { apiToFormErrors, zodToFormErrors } from "@/utils/formErrors"
import type { APIErrorResponse } from "@/types/api"
import type {
  PlantingLocationStatusPayload,
  PlantingLocationStatus,
} from "@/types/plantingLocationStatus"
import { AxiosError } from "axios"
import { computed } from "vue"

const STATUS_LABELS: Record<(typeof MANUAL_STATUS_CHOICES)[number], string> = {
  DAMAGED: "Damaged",
  DESTROYED: "Destroyed",
  RETIRED: "Retired",
}

const open = defineModel<boolean>("open")
const { currentStatus, isLoading, isCreateSuccess } = defineProps<{
  currentStatus: PlantingLocationStatus | null | undefined
  isLoading: boolean
  isCreateSuccess: boolean
}>()

const emit = defineEmits<{
  (e: "submit", payload: PlantingLocationStatusPayload, onError: (err: unknown) => void): void
}>()

const isBlocked = computed(() => currentStatus?.status === "IN_USE")

const formInitialState: PlantingLocationStatusForm = {
  status: "DAMAGED",
  notes: "",
  image: undefined,
}

const form = reactive<PlantingLocationStatusForm>({ ...formInitialState })
const errors = ref<Record<string, string>>({})

const handleImageChange = (event: Event): void => {
  form.image = getFileFromEvent(event)
}

const handleSubmit = (): void => {
  const result = plantingLocationStatusSchema.safeParse(form)

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
  () => open.value,
  (isOpen) => {
    if (!isOpen) resetForm()
  },
)
</script>

<template>
  <Dialog v-model:open="open">
    <form id="set-status-form" @submit.prevent="handleSubmit">
      <DialogContent class="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Set Status</DialogTitle>
          <DialogDescription>Record a new status entry for this location.</DialogDescription>
        </DialogHeader>
        <p v-if="isBlocked" class="text-sm text-muted-foreground text-center py-4">
          Status cannot be changed while this location is in use.
        </p>
        <FieldGroup v-if="!isBlocked">
          <Field>
            <FieldLabel for="status">Status</FieldLabel>
            <Select id="status" v-model="form.status">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem v-for="choice in MANUAL_STATUS_CHOICES" :key="choice" :value="choice">
                  {{ STATUS_LABELS[choice] }}
                </SelectItem>
              </SelectContent>
            </Select>
            <FieldError data-test="statusError" v-if="errors.status">
              {{ errors.status }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel for="notes">Notes</FieldLabel>
            <textarea
              id="notes"
              v-model="form.notes"
              class="border-input placeholder:text-muted-foreground focus-visible:ring-ring flex min-h-[80px] w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 disabled:cursor-not-allowed disabled:opacity-50"
              placeholder="Optional notes about this status..."
            />
            <FieldError data-test="notesError" v-if="errors.notes">
              {{ errors.notes }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel for="image">Image (optional)</FieldLabel>
            <Input id="image" type="file" accept="image/*" @change="handleImageChange" />
            <FieldError data-test="imageError" v-if="errors.image">
              {{ errors.image }}
            </FieldError>
          </Field>
        </FieldGroup>
        <DialogFooter>
          <DialogClose as-child>
            <Button variant="outline" type="button"> Cancel </Button>
          </DialogClose>
          <Button v-if="!isBlocked" type="submit" form="set-status-form">
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
