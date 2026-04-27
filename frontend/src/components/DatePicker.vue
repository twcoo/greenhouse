<script setup lang="ts">
import { computed } from "vue"
import { parseDate, getLocalTimeZone } from "@internationalized/date"
import type { DateValue } from "reka-ui"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Button } from "@/components/ui/button"
import { IconCalendar } from "@tabler/icons-vue"

const { modelValue, placeholder, disabled } = defineProps<{
  modelValue?: string
  placeholder?: string
  disabled?: boolean
}>()

const emit = defineEmits<{
  (e: "update:modelValue", value: string | undefined): void
}>()

const dateValue = computed<DateValue | undefined>(() => {
  if (!modelValue) return undefined
  try {
    return parseDate(modelValue)
  } catch {
    return undefined
  }
})

const displayValue = computed<string>(() => {
  if (!dateValue.value) return placeholder ?? "Pick a date"
  return dateValue.value.toDate(getLocalTimeZone()).toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  })
})

const handleSelect = (value: DateValue | undefined): void => {
  emit("update:modelValue", value?.toString())
}
</script>

<template>
  <Popover>
    <PopoverTrigger as-child>
      <Button
        variant="outline"
        :disabled="disabled"
        class="w-full justify-start text-left font-normal"
        :class="{ 'text-muted-foreground': !modelValue }"
      >
        <IconCalendar class="mr-2 h-4 w-4 shrink-0" />
        {{ displayValue }}
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-auto p-0" align="start">
      <Calendar
        layout="month-and-year"
        :model-value="dateValue"
        @update:model-value="handleSelect"
      />
    </PopoverContent>
  </Popover>
</template>
