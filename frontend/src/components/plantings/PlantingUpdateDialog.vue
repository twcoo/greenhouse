<script setup lang="ts">
import { computed, ref, watch } from "vue"
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
import { plantingSchema, PLANTING_STATUSES, type plantingForm } from "@/schemas/planting.schemas"
import type { PlantingPayload } from "@/types/planting"
import type { APIErrorResponse } from "@/types/api"
import { apiToFormErrors, zodToFormErrors } from "@/utils/formErrors"
import { AxiosError } from "axios"
import { IconLoader2 } from "@tabler/icons-vue"
import { useCrop } from "@/composables/useCrops"
import { useVarieties } from "@/composables/useVarieties"

const open = defineModel<boolean>("open")
const { id, plantingFormInitialState, isLoading, isUpdateSuccess } = defineProps<{
  id: number
  plantingFormInitialState: plantingForm
  isLoading: boolean
  isUpdateSuccess: boolean
}>()

const emit = defineEmits<{
  (e: "submit", id: number, payload: PlantingPayload, onError: (err: unknown) => void): void
}>()

const cropPagination = ref({ pageIndex: 0, pageSize: 100 })
const varietyPagination = ref({ pageIndex: 0, pageSize: 100 })

const { crops } = useCrop(cropPagination)
const { varieties } = useVarieties(varietyPagination)

const selectedCropId = ref<string>(String(plantingFormInitialState.crop))
const selectedVarietyId = ref<string>(String(plantingFormInitialState.variety))
const selectedStatus = ref<string>(plantingFormInitialState.status ?? "ACTIVE")
const errors = ref<Record<string, string>>({})

const filteredVarieties = computed(
  () => varieties.value?.results.filter((v) => String(v.crop) === selectedCropId.value) ?? [],
)

watch(selectedCropId, () => {
  selectedVarietyId.value = ""
})

watch(
  () => plantingFormInitialState,
  (newVal) => {
    selectedCropId.value = String(newVal.crop)
    selectedVarietyId.value = String(newVal.variety)
    selectedStatus.value = newVal.status ?? "ACTIVE"
    errors.value = {}
  },
  { deep: true },
)

const handleSubmit = async (): Promise<void> => {
  const result = plantingSchema.safeParse({
    crop: selectedCropId.value,
    variety: selectedVarietyId.value,
    status: selectedStatus.value,
  })

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
    errors.value = {}
    selectedCropId.value = String(plantingFormInitialState.crop)
    selectedVarietyId.value = String(plantingFormInitialState.variety)
    selectedStatus.value = plantingFormInitialState.status ?? "ACTIVE"
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
    <form id="update-planting-form" @submit.prevent="handleSubmit">
      <DialogContent class="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Update Planting</DialogTitle>
          <DialogDescription>Update the planting details below.</DialogDescription>
        </DialogHeader>
        <FieldGroup>
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
            <FieldError data-test="cropError" v-if="errors.crop">
              {{ errors.crop }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel for="variety">Variety</FieldLabel>
            <Select id="variety" v-model="selectedVarietyId" :disabled="!selectedCropId">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select variety" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem
                  v-for="variety in filteredVarieties"
                  :key="variety.id"
                  :value="String(variety.id)"
                >
                  {{ variety.name }}
                </SelectItem>
              </SelectContent>
            </Select>
            <FieldError data-test="varietyError" v-if="errors.variety">
              {{ errors.variety }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel for="status">Status</FieldLabel>
            <Select id="status" v-model="selectedStatus">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem v-for="s in PLANTING_STATUSES" :key="s" :value="s">
                  {{ s.charAt(0) + s.slice(1).toLowerCase() }}
                </SelectItem>
              </SelectContent>
            </Select>
            <FieldError data-test="statusError" v-if="errors.status">
              {{ errors.status }}
            </FieldError>
          </Field>
        </FieldGroup>
        <DialogFooter>
          <DialogClose as-child>
            <Button variant="outline">Cancel</Button>
          </DialogClose>
          <Button type="submit" form="update-planting-form" :disabled="isLoading">
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
