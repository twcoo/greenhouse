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
import {
  FERTILIZER_TYPE_LABEL,
  HEALTH_BADGE_VARIANT,
  HEALTH_LABEL,
  PEST_PRESSURE_LABEL,
  WATERING_EVENT_LABEL,
} from "./constants"

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
          Logged on {{ formatDate(observation.observationDate) }}
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
            v-if="observation.wateringEvent"
            variant="secondary"
            class="bg-blue-500 text-white dark:bg-blue-600"
          >
            {{ WATERING_EVENT_LABEL[observation.wateringEvent] }}
          </Badge>
          <Badge
            v-if="observation.fertilizerType === 'ORGANIC'"
            variant="secondary"
            class="bg-green-600 text-white dark:bg-green-700"
            >{{ FERTILIZER_TYPE_LABEL["ORGANIC"] }}
          </Badge>
          <Badge
            v-if="observation.fertilizerType === 'SYNTHETIC'"
            variant="secondary"
            class="bg-amber-500 text-white dark:bg-amber-600"
            >{{ FERTILIZER_TYPE_LABEL["SYNTHETIC"] }}
          </Badge>
        </div>

        <!-- Fertilizer detail -->
        <div v-if="observation.fertilizerType !== 'NONE' && observation.fertilizerDetail">
          <span class="text-sm text-muted-foreground">Fertilizer detail</span>
          <p class="text-sm mt-1">{{ observation.fertilizerDetail }}</p>
        </div>

        <Badge
          v-if="observation.pruned"
          variant="secondary"
          class="bg-amber-500 text-white dark:bg-amber-600"
          >Pruned
        </Badge>

        <!-- Pruning detail -->
        <div v-if="observation.pruned && observation.pruningDetail">
          <span class="text-sm text-muted-foreground">Pruning detail</span>
          <p class="text-sm mt-1">{{ observation.pruningDetail }}</p>
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
