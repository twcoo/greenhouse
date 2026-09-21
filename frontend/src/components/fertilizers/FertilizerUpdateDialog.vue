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
  fertilizerSchema,
  FERTILIZER_STATUSES,
  FERTILIZER_TYPES,
  type fertilizerForm,
} from "@/schemas/fertilizer.schemas"
import type { FertilizerPayload } from "@/types/fertilizer"
import type { APIErrorResponse } from "@/types/api"
import { apiToFormErrors, zodToFormErrors } from "@/utils/formErrors"
import { AxiosError } from "axios"
import { IconLoader2, IconPlus, IconX } from "@tabler/icons-vue"
import DatePicker from "@/components/DatePicker.vue"

const open = defineModel<boolean>("open")
const { id, fertilizerFormInitialState, isLoading, isUpdateSuccess } = defineProps<{
  id: number
  fertilizerFormInitialState: fertilizerForm
  isLoading: boolean
  isUpdateSuccess: boolean
}>()

const emit = defineEmits<{
  (e: "submit", id: number, payload: FertilizerPayload, onError: (err: unknown) => void): void
}>()

const form = reactive<{
  name: string
  type: "SWAMP" | "COMPOST" | "OTHER"
  status: "BREWING" | "READY" | "USED" | "DISCARDED"
  startDate: string
  ingredients: string[]
  notes: string
}>({
  name: fertilizerFormInitialState.name,
  type: fertilizerFormInitialState.type,
  status: fertilizerFormInitialState.status,
  startDate: fertilizerFormInitialState.startDate,
  ingredients: [...(fertilizerFormInitialState.ingredients ?? [])],
  notes: fertilizerFormInitialState.notes ?? "",
})

const ingredientInput = ref<string>("")
const errors = ref<Record<string, string>>({})

const addIngredient = (): void => {
  const value = ingredientInput.value.trim()
  if (value && !form.ingredients.includes(value)) {
    form.ingredients.push(value)
  }
  ingredientInput.value = ""
}

const removeIngredient = (value: string): void => {
  form.ingredients = form.ingredients.filter((v) => v !== value)
}

watch(
  () => fertilizerFormInitialState,
  (newVal) => {
    form.name = newVal.name
    form.type = newVal.type
    form.status = newVal.status
    form.startDate = newVal.startDate
    form.ingredients = [...(newVal.ingredients ?? [])]
    form.notes = newVal.notes ?? ""
    ingredientInput.value = ""
    errors.value = {}
  },
  { deep: true },
)

const handleSubmit = async (): Promise<void> => {
  const result = fertilizerSchema.safeParse({
    name: form.name,
    type: form.type,
    status: form.status,
    startDate: form.startDate,
    ingredients: [...form.ingredients],
    notes: form.notes,
  })

  if (!result.success) {
    errors.value = zodToFormErrors(result.error)
    return
  }

  const payload: FertilizerPayload = result.data as FertilizerPayload

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
    ingredientInput.value = ""
    form.name = fertilizerFormInitialState.name
    form.type = fertilizerFormInitialState.type
    form.status = fertilizerFormInitialState.status
    form.startDate = fertilizerFormInitialState.startDate
    form.ingredients = [...(fertilizerFormInitialState.ingredients ?? [])]
    form.notes = fertilizerFormInitialState.notes ?? ""
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
    <form id="update-fertilizer-form" @submit.prevent="handleSubmit">
      <DialogContent class="sm:max-w-[500px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Update Fertilizer</DialogTitle>
          <DialogDescription>Update the fertilizer details below.</DialogDescription>
        </DialogHeader>
        <FieldGroup>
          <Field>
            <FieldLabel for="name">Name</FieldLabel>
            <Input id="name" v-model="form.name" />
            <FieldError data-test="nameError" v-if="errors.name">
              {{ errors.name }}
            </FieldError>
          </Field>

          <div class="grid grid-cols-2 gap-4">
            <Field>
              <FieldLabel for="type">Type</FieldLabel>
              <Select id="type" v-model="form.type">
                <SelectTrigger class="w-full">
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem v-for="t in FERTILIZER_TYPES" :key="t" :value="t">
                    {{ t.charAt(0) + t.slice(1).toLowerCase() }}
                  </SelectItem>
                </SelectContent>
              </Select>
              <FieldError data-test="typeError" v-if="errors.type">
                {{ errors.type }}
              </FieldError>
            </Field>
            <Field>
              <FieldLabel for="status">Status</FieldLabel>
              <Select id="status" v-model="form.status">
                <SelectTrigger class="w-full">
                  <SelectValue placeholder="Select status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem v-for="s in FERTILIZER_STATUSES" :key="s" :value="s">
                    {{ s.charAt(0) + s.slice(1).toLowerCase() }}
                  </SelectItem>
                </SelectContent>
              </Select>
              <FieldError data-test="statusError" v-if="errors.status">
                {{ errors.status }}
              </FieldError>
            </Field>
          </div>

          <Field>
            <FieldLabel for="startDate">Start Date</FieldLabel>
            <DatePicker id="startDate" v-model="form.startDate" />
            <FieldError data-test="startDateError" v-if="errors.startDate">
              {{ errors.startDate }}
            </FieldError>
          </Field>

          <Field>
            <FieldLabel for="ingredientInput">Ingredients</FieldLabel>
            <div class="flex items-center gap-2">
              <Input
                id="ingredientInput"
                v-model="ingredientInput"
                placeholder="e.g. banana peels"
                @keydown.enter.prevent="addIngredient"
              />
              <Button type="button" variant="outline" @click="addIngredient">
                <IconPlus :size="16" />
              </Button>
            </div>
            <div v-if="form.ingredients.length" class="flex flex-wrap gap-1 mt-2">
              <span
                v-for="ingredient in form.ingredients"
                :key="ingredient"
                class="inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs"
              >
                {{ ingredient }}
                <button
                  type="button"
                  data-test="remove-ingredient"
                  class="text-muted-foreground hover:text-foreground"
                  @click="removeIngredient(ingredient)"
                >
                  <IconX :size="12" />
                </button>
              </span>
            </div>
            <FieldError data-test="ingredientsError" v-if="errors.ingredients">
              {{ errors.ingredients }}
            </FieldError>
          </Field>

          <Field>
            <FieldLabel for="notes">Notes</FieldLabel>
            <textarea
              id="notes"
              v-model="form.notes"
              class="border-input placeholder:text-muted-foreground focus-visible:ring-ring flex min-h-[80px] w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-1 disabled:cursor-not-allowed disabled:opacity-50"
              placeholder="Optional notes about this fertilizer..."
            />
          </Field>
        </FieldGroup>
        <DialogFooter>
          <DialogClose as-child>
            <Button variant="outline" type="button">Cancel</Button>
          </DialogClose>
          <Button type="submit" form="update-fertilizer-form" :disabled="isLoading">
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
