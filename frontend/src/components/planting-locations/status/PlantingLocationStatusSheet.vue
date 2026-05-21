<script setup lang="ts">
import { computed, ref, toRef, watch } from "vue"
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet"
import { Dialog, DialogContent } from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { IconLoader2, IconPlus } from "@tabler/icons-vue"
import PlantingLocationSetStatusDialog from "./PlantingLocationSetStatusDialog.vue"
import { usePlantingLocationStatuses } from "@/composables/usePlantingLocationStatuses"
import type {
  PlantingLocationStatus,
  PlantingLocationStatusChoice,
  PlantingLocationStatusPayload,
} from "@/types/plantingLocationStatus"
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
const { locationId, currentStatus } = defineProps<{
  locationId: number
  currentStatus: PlantingLocationStatus | null | undefined
}>()

const isBlocked = computed(() => currentStatus?.status === "IN_USE")

const pagination = ref({ pageIndex: 0, pageSize: 10 })

const { statuses, isLoading, isCreateSuccess, createStatus } = usePlantingLocationStatuses(
  toRef(() => locationId),
  pagination,
)

const totalPages = computed(() =>
  Math.ceil((statuses.value?.count ?? 0) / pagination.value.pageSize),
)

const hasStatuses = computed(() => (statuses.value?.results?.length ?? 0) > 0)

const openSetStatusDialog = ref(false)

const handleCreate = async (
  payload: PlantingLocationStatusPayload,
  onError: (err: unknown) => void,
): Promise<void> => {
  try {
    await createStatus({ id: locationId, payload })
  } catch (err) {
    onError(err)
  }
}

const previewOpen = ref(false)
const previewImage = ref<string | null>(null)

const openPreview = (url: string): void => {
  previewImage.value = url
  previewOpen.value = true
}

const closePreview = (): void => {
  previewOpen.value = false
  setTimeout(() => {
    previewImage.value = null
  }, 200)
}

watch(
  () => isCreateSuccess.value,
  (success) => {
    if (success) {
      pagination.value.pageIndex = 0
    }
  },
)
</script>

<template>
  <Sheet v-model:open="open">
    <SheetContent class="sm:max-w-lg w-full flex flex-col gap-4 px-4">
      <SheetHeader>
        <SheetTitle>Location Status</SheetTitle>
        <SheetDescription>View and manage status entries for this location.</SheetDescription>
      </SheetHeader>

      <div class="flex justify-end">
        <Button
          variant="outline"
          size="sm"
          :disabled="isBlocked"
          @click="openSetStatusDialog = true"
          data-test="set-status-button"
        >
          <IconPlus :size="16" />
          <span>Set Status</span>
        </Button>
      </div>

      <div
        v-if="isLoading && !hasStatuses"
        data-test="loading-container"
        class="flex flex-col items-center justify-center py-8"
      >
        <IconLoader2 class="animate-spin h-8 w-8 mb-2" />
        <span class="text-sm text-muted-foreground">Loading status history...</span>
      </div>

      <div
        v-else-if="!hasStatuses"
        data-test="empty-state"
        class="text-sm text-muted-foreground text-center py-6"
      >
        No status entries recorded yet.
      </div>

      <ul v-else class="space-y-3 overflow-y-auto pr-1" data-test="status-list">
        <li
          v-for="entry in statuses?.results"
          :key="entry.id"
          class="flex gap-3 border rounded-md p-3"
        >
          <button
            v-if="entry.image"
            type="button"
            class="flex-shrink-0 rounded overflow-hidden focus:outline-none focus:ring-2 focus:ring-ring cursor-zoom-in"
            @click="openPreview(entry.image!)"
            data-test="image-thumbnail"
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

      <div
        v-if="hasStatuses"
        class="flex items-center justify-between gap-4 py-4"
        data-test="pagination"
      >
        <div class="text-sm font-medium" data-test="page-info">
          Page {{ pagination.pageIndex + 1 }} of {{ totalPages }}
        </div>
        <div class="flex items-center gap-1">
          <Button
            size="sm"
            variant="outline"
            :disabled="pagination.pageIndex === 0"
            @click="pagination.pageIndex--"
            data-test="prev-button"
          >
            Previous
          </Button>
          <Button
            size="sm"
            variant="outline"
            :disabled="pagination.pageIndex + 1 >= totalPages"
            @click="pagination.pageIndex++"
            data-test="next-button"
          >
            Next
          </Button>
        </div>
      </div>
    </SheetContent>
  </Sheet>

  <!-- Set Status Dialog -->
  <PlantingLocationSetStatusDialog
    v-if="openSetStatusDialog"
    v-model:open="openSetStatusDialog"
    :currentStatus="currentStatus"
    :isLoading="isLoading"
    :isCreateSuccess="isCreateSuccess"
    @submit="handleCreate"
  />

  <!-- Image Preview Dialog -->
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
