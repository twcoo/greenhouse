<script setup lang="ts">
import { ref, watch } from "vue"
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
import { fertilizerLogSchema, type FertilizerLogForm } from "@/schemas/fertilizerLog.schemas"
import type { APIErrorResponse } from "@/types/api"
import { apiToFormErrors, zodToFormErrors } from "@/utils/formErrors"
import { AxiosError } from "axios"
import { IconLoader2 } from "@tabler/icons-vue"
import { EVENT_TYPE_OPTIONS } from "./constants"
import DatePicker from "@/components/DatePicker.vue"
import { today, getLocalTimeZone } from "@internationalized/date"

const open = defineModel<boolean>("open")
const { isLoading, isCreateSuccess, fertilizerName } = defineProps<{
  isLoading: boolean
  isCreateSuccess: boolean
  fertilizerName: string
}>()

const emit = defineEmits<{
  (e: "submit", payload: FertilizerLogForm, onError: (err: unknown) => void): void
}>()

const formInitialState: FertilizerLogForm = {
  logDate: today(getLocalTimeZone()).toString(),
  eventType: "OTHER",
  itemAdded: "",
  quantity: "",
  notes: "",
}

const form = ref<FertilizerLogForm>({ ...formInitialState })
const errors = ref<Record<string, string>>({})

const handleSubmit = (): void => {
  const result = fertilizerLogSchema.safeParse(form.value)

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
  form.value = { ...formInitialState }
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

watch(open, (isOpen) => {
  if (isOpen) resetForm()
})
</script>

<template>
  <Dialog v-model:open="open">
    <form id="fertilizer-log-create-form" @submit.prevent="handleSubmit">
      <DialogContent class="sm:max-w-[450px]">
        <DialogHeader>
          <DialogTitle>Log Entry</DialogTitle>
          <DialogDescription> Record what was added to {{ fertilizerName }}. </DialogDescription>
        </DialogHeader>

        <FieldGroup>
          <Field>
            <FieldLabel for="logDate">Date</FieldLabel>
            <DatePicker id="logDate" v-model="form.logDate" />
            <FieldError data-test="logDateError" v-if="errors.logDate">
              {{ errors.logDate }}
            </FieldError>
          </Field>

          <Field>
            <FieldLabel for="eventType">Event Type</FieldLabel>
            <Select id="eventType" v-model="form.eventType">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select event type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem v-for="opt in EVENT_TYPE_OPTIONS" :key="opt.value" :value="opt.value">
                  {{ opt.label }}
                </SelectItem>
              </SelectContent>
            </Select>
            <FieldError data-test="eventTypeError" v-if="errors.eventType">
              {{ errors.eventType }}
            </FieldError>
          </Field>

          <div class="grid grid-cols-2 gap-4">
            <Field>
              <FieldLabel for="itemAdded">Item Added</FieldLabel>
              <Input id="itemAdded" v-model="form.itemAdded" placeholder="e.g. banana peels" />
            </Field>
            <Field>
              <FieldLabel for="quantity">Quantity</FieldLabel>
              <Input id="quantity" v-model="form.quantity" placeholder="e.g. 2 kg" />
            </Field>
          </div>

          <Field>
            <FieldLabel for="notes">Notes</FieldLabel>
            <textarea
              id="notes"
              v-model="form.notes"
              class="border-input placeholder:text-muted-foreground focus-visible:ring-ring flex min-h-[80px] w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 disabled:cursor-not-allowed disabled:opacity-50"
              placeholder="Optional notes..."
            />
          </Field>
        </FieldGroup>

        <DialogFooter>
          <DialogClose as-child>
            <Button variant="outline" type="button">Cancel</Button>
          </DialogClose>
          <Button type="submit" form="fertilizer-log-create-form" :disabled="isLoading">
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
