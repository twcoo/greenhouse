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
        <div>
          <div class="flex items-center gap-2">
            <span class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Health</span
            >
            <div class="flex-1 h-px bg-border" />
          </div>
          <div class="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1.5 text-sm mt-2">
            <span class="text-muted-foreground">Status</span>
            <span>
              <Badge :variant="HEALTH_BADGE_VARIANT[observation.healthStatus]">
                {{ HEALTH_LABEL[observation.healthStatus] }}
              </Badge>
            </span>
            <span class="text-muted-foreground">Pest pressure</span>
            <span>{{ PEST_PRESSURE_LABEL[observation.pestPressure] }}</span>
            <template v-if="observation.diseaseSymptoms">
              <span class="text-muted-foreground">Disease</span>
              <span class="text-destructive">Present</span>
            </template>
          </div>
        </div>

        <!-- Watering -->
        <div v-if="observation.wateringEvent">
          <div class="flex items-center gap-2">
            <span class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Watering</span
            >
            <div class="flex-1 h-px bg-border" />
          </div>
          <div class="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1.5 text-sm mt-2">
            <span class="text-muted-foreground">Event</span>
            <span>
              <Badge variant="secondary" class="bg-blue-500 text-white dark:bg-blue-600">
                {{ WATERING_EVENT_LABEL[observation.wateringEvent] }}
              </Badge>
            </span>
          </div>
        </div>

        <!-- Pruning -->
        <div v-if="observation.pruned">
          <div class="flex items-center gap-2">
            <span class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Pruning</span
            >
            <div class="flex-1 h-px bg-border" />
          </div>
          <div class="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1.5 text-sm mt-2">
            <template v-if="observation.pruningDetail">
              <span class="text-muted-foreground">Detail</span>
              <span>{{ observation.pruningDetail }}</span>
            </template>
            <template v-else>
              <span class="text-muted-foreground">Pruned</span>
              <span>Yes</span>
            </template>
          </div>
        </div>

        <!-- Fertilization -->
        <div v-if="observation.fertilizerType !== 'NONE'">
          <div class="flex items-center gap-2">
            <span class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Fertilization</span
            >
            <div class="flex-1 h-px bg-border" />
          </div>
          <div class="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1.5 text-sm mt-2">
            <span class="text-muted-foreground">Type</span>
            <span>
              <Badge
                v-if="observation.fertilizerType === 'ORGANIC'"
                variant="secondary"
                class="bg-green-600 text-white dark:bg-green-700"
              >
                {{ FERTILIZER_TYPE_LABEL["ORGANIC"] }}
              </Badge>
              <Badge
                v-else-if="observation.fertilizerType === 'SYNTHETIC'"
                variant="secondary"
                class="bg-amber-500 text-white dark:bg-amber-600"
              >
                {{ FERTILIZER_TYPE_LABEL["SYNTHETIC"] }}
              </Badge>
            </span>
            <template v-if="observation.fertilizerDetail">
              <span class="text-muted-foreground">Detail</span>
              <span>{{ observation.fertilizerDetail }}</span>
            </template>
          </div>
        </div>

        <!-- Notes -->
        <div v-if="observation.notes">
          <div class="flex items-center gap-2">
            <span class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Notes</span
            >
            <div class="flex-1 h-px bg-border" />
          </div>
          <p class="text-sm mt-2">{{ observation.notes }}</p>
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
