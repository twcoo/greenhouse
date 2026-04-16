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

import type { VarietyPayload } from "@/types/variety"
import type { APIErrorResponse } from "@/types/api"
import { FieldGroup, Field, FieldLabel, FieldError } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { varietySchema, type varietyForm } from "@/schemas/variety.schemas"
import { apiToFormErrors, zodToFormErrors } from "@/utils/formErrors"
import { AxiosError } from "axios"
import { IconLoader2 } from "@tabler/icons-vue"
import { useCrop } from "@/composables/useCrops"

const open = defineModel<boolean>("open")
const { isLoading, isCreateSuccess } = defineProps<{
  isLoading: boolean
  isCreateSuccess: boolean
}>()

const emit = defineEmits<{
  (e: "submit", payload: VarietyPayload, onError: (err: unknown) => void): void
}>()

const cropPagination = ref({ pageIndex: 0, pageSize: 100 })
const { crops } = useCrop(cropPagination)

const form = reactive<varietyForm>({ name: "", crop: 1, growthHabit: ["DETERMINATE"] })
const selectedCropId = ref<string>("")
const errors = ref<Record<string, string>>({})

const toggleGrowthHabit = (value: "DETERMINATE" | "INDETERMINATE", checked: boolean): void => {
  if (checked) {
    if (!form.growthHabit.includes(value)) {
      form.growthHabit.push(value)
    }
  } else {
    form.growthHabit = form.growthHabit.filter((v) => v !== value)
  }
}

const handleSubmit = async (): Promise<void> => {
  const result = varietySchema.safeParse({
    name: form.name,
    crop: selectedCropId.value,
    growthHabit: [...form.growthHabit],
  })

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
  form.name = ""
  form.growthHabit = []
  selectedCropId.value = ""
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
</script>

<template>
  <Dialog v-model:open="open">
    <form id="variety-form" @submit.prevent="handleSubmit">
      <DialogContent class="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add Variety</DialogTitle>
          <DialogDescription>
            Add a new variety to your list. Fill in the details below.
          </DialogDescription>
        </DialogHeader>
        <FieldGroup>
          <Field>
            <FieldLabel for="name">Name</FieldLabel>
            <Input v-model="form.name" id="name" name="name" />
            <FieldError data-test="name" v-if="errors.name">
              {{ errors.name }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel for="crop">Crop</FieldLabel>
            <Select id="crop" v-model="selectedCropId">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select crop" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem v-for="crop in crops?.results" :key="crop.id" :value="String(crop.id)">
                  {{ crop.name }}
                </SelectItem>
              </SelectContent>
            </Select>
            <FieldError data-test="crop" v-if="errors.crop">
              {{ errors.crop }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel>Growth Habit</FieldLabel>
            <div class="flex flex-col gap-2 mt-1">
              <div class="flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  id="create-determinate"
                  :checked="form.growthHabit.includes('DETERMINATE')"
                  @change="
                    toggleGrowthHabit('DETERMINATE', ($event.target as HTMLInputElement).checked)
                  "
                  class="h-4 w-4 rounded border border-input cursor-pointer accent-primary"
                />
                <label for="create-determinate" class="cursor-pointer">Determinate</label>
              </div>
              <div class="flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  id="create-indeterminate"
                  :checked="form.growthHabit.includes('INDETERMINATE')"
                  @change="
                    toggleGrowthHabit('INDETERMINATE', ($event.target as HTMLInputElement).checked)
                  "
                  class="h-4 w-4 rounded border border-input cursor-pointer accent-primary"
                />
                <label for="create-indeterminate" class="cursor-pointer">Indeterminate</label>
              </div>
            </div>
            <FieldError data-test="growthHabit" v-if="errors.growthHabit">
              {{ errors.growthHabit }}
            </FieldError>
          </Field>
        </FieldGroup>
        <DialogFooter>
          <DialogClose as-child>
            <Button variant="outline"> Cancel </Button>
          </DialogClose>
          <Button type="submit" form="variety-form">
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
