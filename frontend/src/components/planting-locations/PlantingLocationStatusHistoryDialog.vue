<script setup lang="ts">
import { computed, ref } from "vue"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import { IconLoader2 } from "@tabler/icons-vue"
import { usePlantingLocationStatuses } from "@/composables/usePlantingLocationStatuses"
import type { PlantingLocationStatusChoice } from "@/types/plantingLocationStatus"
import { formatDate } from "@/utils/formatting"

const STATUS_BADGE_VARIANT: Record<
  PlantingLocationStatusChoice,
  "secondary" | "default" | "destructive" | "outline"
> = {
  AVAILABLE: "secondary",
  IN_USE: "default",
  DAMAGED: "outline",
  DESTROYED: "destructive",
  RETIRED: "destructive",
}

const STATUS_LABEL: Record<PlantingLocationStatusChoice, string> = {
  AVAILABLE: "Available",
  IN_USE: "In Use",
  DAMAGED: "Damaged",
  DESTROYED: "Destroyed",
  RETIRED: "Retired",
}

const open = defineModel<boolean>("open")
const { locationId } = defineProps<{ locationId: number | null }>()

const locationIdRef = computed(() => locationId)
const { statuses, isLoading } = usePlantingLocationStatuses(locationIdRef)

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
        <DialogTitle>Status History</DialogTitle>
        <DialogDescription>Past status entries for this location.</DialogDescription>
      </DialogHeader>

      <div v-if="isLoading" class="flex justify-center py-6">
        <IconLoader2 class="animate-spin h-6 w-6" />
      </div>

      <div
        v-else-if="!statuses?.results?.length"
        class="text-sm text-muted-foreground text-center py-6"
      >
        No status entries recorded yet.
      </div>

      <ul v-else class="space-y-3 max-h-96 overflow-y-auto pr-1">
        <li
          v-for="entry in statuses.results"
          :key="entry.id"
          class="flex gap-3 border rounded-md p-3"
        >
          <button
            v-if="entry.image"
            type="button"
            class="flex-shrink-0 rounded overflow-hidden focus:outline-none focus:ring-2 focus:ring-ring cursor-zoom-in"
            @click="openPreview(entry.image!)"
          >
            <img :src="entry.image" alt="Status image" class="h-14 w-14 rounded object-cover" />
          </button>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <Badge :variant="STATUS_BADGE_VARIANT[entry.status as PlantingLocationStatusChoice]">
                {{ STATUS_LABEL[entry.status as PlantingLocationStatusChoice] }}
              </Badge>
              <span class="text-xs text-muted-foreground">{{ formatDate(entry.createdAt) }}</span>
            </div>
            <p v-if="entry.notes" class="text-sm text-foreground truncate">{{ entry.notes }}</p>
          </div>
        </li>
      </ul>
    </DialogContent>
  </Dialog>

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
        alt="Status image full size"
        class="w-full rounded-lg object-contain max-h-[60vh]"
      />
    </DialogContent>
  </Dialog>
</template>
