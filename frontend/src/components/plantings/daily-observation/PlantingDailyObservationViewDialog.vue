<script setup lang="ts">
import { ref } from "vue"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import { formatDate } from "@/utils/formatting"
import type { PlantingDailyObservation } from "@/types/plantingDailyObservation"
import { HEALTH_BADGE_VARIANT, HEALTH_LABEL, PEST_PRESSURE_LABEL } from "./constants"

const open = defineModel<boolean>("open")
const { observation } = defineProps<{ observation: PlantingDailyObservation | null }>()

const previewOpen = ref(false)
const previewImage = ref<string | null>(null)

const openPreview = (url: string) => {
  previewImage.value = url
  previewOpen.value = true
}

const closePreview = (): void => {
  previewOpen.value = false
  setTimeout(() => {
    previewImage.value = null
  }, 200)
}
</script>

<template>
  <Dialog v-model:open="open">
    <DialogContent class="sm:max-w-[500px]">
      <DialogHeader>
        <DialogTitle>Observation Details</DialogTitle>
        <DialogDescription v-if="observation">
          Logged on {{ formatDate(observation.createdAt) }}
        </DialogDescription>
      </DialogHeader>

      <div v-if="observation" class="space-y-4">
        <!-- Image -->
        <button
          v-if="observation.image"
          type="button"
          class="block rounded overflow-hidden focus:outline-none focus:ring-2 focus:ring-ring cursor-zoom-in"
          @click="openPreview(observation.image!)"
        >
          <img
            :src="observation.image"
            alt="Observation image"
            class="w-full max-h-48 object-cover rounded"
          />
        </button>

        <!-- Health -->
        <div class="flex items-center gap-2">
          <Badge :variant="HEALTH_BADGE_VARIANT[observation.healthStatus]">
            {{ HEALTH_LABEL[observation.healthStatus] }}
          </Badge>
          <span class="text-sm text-muted-foreground">
            Pest pressure: {{ PEST_PRESSURE_LABEL[observation.pestPressure] }}
          </span>
          <span v-if="observation.diseaseSymptoms" class="text-sm text-destructive">
            · Disease symptoms present
          </span>
          <Badge
            v-if="observation.watered"
            variant="secondary"
            class="bg-blue-500 text-white dark:bg-blue-600"
            >Watered
          </Badge>
        </div>

        <!-- Detail grid -->
        <div class="grid grid-cols-2 gap-x-6 gap-y-2 text-sm">
          <div>
            <span class="text-muted-foreground">Height (cm)</span>
            <p class="font-medium">{{ observation.heightCm ?? "—" }}</p>
          </div>
          <div>
            <span class="text-muted-foreground">Leaf count</span>
            <p class="font-medium">{{ observation.leafCount ?? "—" }}</p>
          </div>
          <div>
            <span class="text-muted-foreground">Temperature (°C)</span>
            <p class="font-medium">{{ observation.temperatureC ?? "—" }}</p>
          </div>
          <div>
            <span class="text-muted-foreground">Humidity (%)</span>
            <p class="font-medium">{{ observation.humidityPercent ?? "—" }}</p>
          </div>
          <div>
            <span class="text-muted-foreground">Light hours</span>
            <p class="font-medium">{{ observation.lightHours ?? "—" }}</p>
          </div>
          <div>
            <span class="text-muted-foreground">Soil moisture (%)</span>
            <p class="font-medium">{{ observation.soilMoisturePercent ?? "—" }}</p>
          </div>
          <div>
            <span class="text-muted-foreground">Soil pH</span>
            <p class="font-medium">{{ observation.soilPh ?? "—" }}</p>
          </div>
          <div>
            <span class="text-muted-foreground">EC (mS/cm)</span>
            <p class="font-medium">{{ observation.ecMsCm ?? "—" }}</p>
          </div>
        </div>

        <!-- Notes -->
        <div v-if="observation.notes">
          <span class="text-sm text-muted-foreground">Notes</span>
          <p class="text-sm mt-1">{{ observation.notes }}</p>
        </div>
      </div>
    </DialogContent>
  </Dialog>

  <!-- Image zoom preview -->
  <Dialog
    :open="previewOpen"
    @update:open="
      (v) => {
        if (!v) closePreview()
      }
    "
  >
    <DialogContent class="sm:max-w-lg p-4">
      <img
        :src="previewImage ?? undefined"
        alt="Observation image full size"
        class="w-full rounded-lg object-contain max-h-[60vh]"
      />
    </DialogContent>
  </Dialog>
</template>
