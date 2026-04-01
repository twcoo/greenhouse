<script setup lang="ts">
import { computed, reactive, ref, watch } from "vue"
import { Button } from "@/components/ui/button"
import { IconPlus } from "@tabler/icons-vue"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
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
import { cropsSchema, type cropsForm } from "@/schemas/crops.schemas"
import type { cropPayload } from "@/types/crop"
import { zodToFormErrors } from "@/utils/formErrors"
import { IconLoader2 } from "@tabler/icons-vue"

const props = defineProps<{
  mode: "create" | "edit"
  loading: boolean
}>()

const emit = defineEmits<{ (e: "submit", payload: cropPayload): void }>()
const actionLabel = computed(() => (props.mode === "create" ? "Add" : "Update"))
const isDialogOpen = ref<boolean>(false)

const formInitialState: cropsForm = {
  name: "",
  scientificName: "",
  category: "VEGETABLE",
  sunlightRequirement: "FULL SUN",
  minDaysToHarvest: 0,
  maxDaysToHarvest: 0,
}

const form = reactive<cropsForm>({ ...formInitialState })

const errors = ref<Record<string, string>>({})

function resetForm() {
  Object.assign(form, formInitialState)
  errors.value = {}
}

async function handleSubmit(): Promise<void> {
  const result = cropsSchema.safeParse(form)

  if (!result.success) {
    errors.value = zodToFormErrors(result.error)
    return
  }

  emit("submit", result.data)
}

watch(
  () => props.loading,
  (isLoading: boolean) => {
    if (!isLoading) {
      isDialogOpen.value = false
      resetForm()
    }
  },
)
</script>

<template>
  <Dialog v-model:open="isDialogOpen">
    <form id="crop-form" @submit.prevent="handleSubmit">
      <DialogTrigger as-child>
        <Button variant="outline">
          <IconPlus />
          <span class="hidden lg:inline">{{ actionLabel }} Crop</span>
        </Button>
      </DialogTrigger>
      <DialogContent class="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{{ actionLabel }} Crop</DialogTitle>
          <DialogDescription>
            {{
              mode === "create"
                ? "Add a new crop to your list. Fill in the details below."
                : "Update the details of this crop. Click save when you're done."
            }}
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
            <FieldLabel for="name">Scientific Name</FieldLabel>
            <Input v-model="form.scientificName" id="scientificName" name="scientificName" />
            <FieldError data-test="scientificName" v-if="errors.scientificName">
              {{ errors.scientificName }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel for="category">Category</FieldLabel>
            <Select id="category" v-model="form.category">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="VEGETABLE"> Vegetable </SelectItem>
                <SelectItem value="FRUIT"> Fruit </SelectItem>
              </SelectContent>
            </Select>
            <FieldError data-test="category" v-if="errors.category">
              {{ errors.category }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel for="sunlightRequirement">Sunlight Requirement</FieldLabel>
            <Select id="sunlightRequirement" v-model="form.sunlightRequirement">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select sunlight requirement" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="FULL SUN"> Full Sun </SelectItem>
                <SelectItem value="PART SUN"> Partial Sun </SelectItem>
                <SelectItem value="FULL SHADE"> Full Shade </SelectItem>
              </SelectContent>
            </Select>
            <FieldError data-test="sunlightRequirement" v-if="errors.sunlightRequirement">
              {{ errors.sunlightRequirement }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel for="minDaysToHarvest">Min Days To Harvest</FieldLabel>
            <Input
              v-model="form.minDaysToHarvest"
              type="number"
              id="minDaysToHarvest"
              name="minDaysToHarvest"
            />
            <FieldError data-test="minDaysToHarvest" v-if="errors.minDaysToHarvest">
              {{ errors.minDaysToHarvest }}
            </FieldError>
          </Field>
          <Field>
            <FieldLabel for="maxDaysToHarvest">Max Days To Harvest</FieldLabel>
            <Input
              v-model="form.maxDaysToHarvest"
              type="number"
              id="maxDaysToHarvest"
              name="maxDaysToHarvest"
            />
            <FieldError data-test="maxDaysToHarvest" v-if="errors.maxDaysToHarvest">
              {{ errors.maxDaysToHarvest }}
            </FieldError>
          </Field>
        </FieldGroup>
        <DialogFooter>
          <DialogClose as-child>
            <Button variant="outline"> Cancel </Button>
          </DialogClose>
          <Button type="submit" form="crop-form">
            <IconLoader2 v-if="loading" :size="18" class="animate-spin" />
            {{ loading ? "Saving..." : "Save" }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </form>
  </Dialog>
</template>
