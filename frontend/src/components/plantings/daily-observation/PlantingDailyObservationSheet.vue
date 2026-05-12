<script setup lang="ts">
import { computed, ref, toRef } from "vue"
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet"
import {
  Table,
  TableBody,
  TableCell,
  TableEmpty,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { IconEye, IconLoader2, IconPencil, IconPlus, IconTrash } from "@tabler/icons-vue"
import PlantingDailyObservationCreateDialog from "./PlantingDailyObservationCreateDialog.vue"
import PlantingDailyObservationUpdateDialog from "./PlantingDailyObservationUpdateDialog.vue"
import PlantingDailyObservationViewDialog from "./PlantingDailyObservationViewDialog.vue"
import { usePlantingDailyObservations } from "@/composables/usePlantingDailyObservations"
import type { PlantingDailyObservation, HealthStatus } from "@/types/plantingDailyObservation"
import type { PlantingDailyObservationForm } from "@/schemas/plantingDailyObservation.schemas"
import { formatDate } from "@/utils/formatting"
import { HEALTH_BADGE_VARIANT, HEALTH_LABEL } from "./constants"

const open = defineModel<boolean>("open")
const { plantingId } = defineProps<{ plantingId: number }>()

const pagination = ref({ pageIndex: 0, pageSize: 10 })

const {
  observations,
  isLoading,
  isCreateSuccess,
  isUpdateSuccess,
  createObservation,
  updateObservation,
  deleteObservation,
} = usePlantingDailyObservations(
  toRef(() => plantingId),
  pagination,
)

const totalPages = computed(() =>
  Math.ceil((observations.value?.count ?? 0) / pagination.value.pageSize),
)

// Create dialog
const openCreateDialog = ref<boolean>(false)

// Update dialog
const openUpdateDialog = ref<boolean>(false)
const observationIdToUpdate = ref<number>(0)
const observationUpdateFormState = ref<PlantingDailyObservationForm | null>(null)

// View dialog
const openViewDialog = ref<boolean>(false)
const observationToView = ref<PlantingDailyObservation | null>(null)

// Delete dialog
const isDeleteDialogOpen = ref<boolean>(false)
const observationIdToDelete = ref<number>(0)

const setViewDialog = (obs: PlantingDailyObservation): void => {
  observationToView.value = obs
  openViewDialog.value = true
}

const setUpdateDialog = (id: number, form: PlantingDailyObservationForm): void => {
  observationIdToUpdate.value = id
  observationUpdateFormState.value = form
  openUpdateDialog.value = true
}

const confirmDelete = (id: number): void => {
  observationIdToDelete.value = id
  isDeleteDialogOpen.value = true
}

const handleCreate = async (
  payload: PlantingDailyObservationForm,
  onError: (err: unknown) => void,
): Promise<void> => {
  try {
    await createObservation(payload)
    pagination.value.pageIndex = 0
  } catch (err) {
    onError(err)
  }
}

const handleUpdate = async (
  id: number,
  payload: PlantingDailyObservationForm,
  onError: (err: unknown) => void,
): Promise<void> => {
  try {
    await updateObservation({ id, payload })
  } catch (err) {
    onError(err)
  }
}

const handleDelete = async (): Promise<void> => {
  await deleteObservation(observationIdToDelete.value)
  isDeleteDialogOpen.value = false
  pagination.value.pageIndex = 0
}

const toObservationForm = (obs: {
  healthStatus: string
  pestPressure: string
  diseaseSymptoms: boolean
  heightCm: string | null
  leafCount: number | null
  temperatureC: string | null
  humidityPercent: string | null
  lightHours: string | null
  soilMoisturePercent: string | null
  soilPh: string | null
  ecMsCm: string | null
  notes: string
}): PlantingDailyObservationForm => ({
  healthStatus: obs.healthStatus as HealthStatus,
  pestPressure: obs.pestPressure as "NONE" | "LOW" | "MEDIUM" | "HIGH",
  diseaseSymptoms: obs.diseaseSymptoms,
  heightCm: obs.heightCm !== null ? Number(obs.heightCm) : undefined,
  leafCount: obs.leafCount ?? undefined,
  temperatureC: obs.temperatureC !== null ? Number(obs.temperatureC) : undefined,
  humidityPercent: obs.humidityPercent !== null ? Number(obs.humidityPercent) : undefined,
  lightHours: obs.lightHours !== null ? Number(obs.lightHours) : undefined,
  soilMoisturePercent:
    obs.soilMoisturePercent !== null ? Number(obs.soilMoisturePercent) : undefined,
  soilPh: obs.soilPh !== null ? Number(obs.soilPh) : undefined,
  ecMsCm: obs.ecMsCm !== null ? Number(obs.ecMsCm) : undefined,
  notes: obs.notes ?? "",
  image: undefined,
})

const hasObservations = computed(() => (observations.value?.results?.length ?? 0) > 0)
</script>

<template>
  <Sheet v-model:open="open">
    <SheetContent class="sm:max-w-lg w-full flex flex-col gap-4">
      <SheetHeader>
        <SheetTitle>Daily Observations</SheetTitle>
        <SheetDescription>Log and manage daily observations for this planting.</SheetDescription>
      </SheetHeader>

      <div class="flex justify-end">
        <Button variant="outline" size="sm" @click="openCreateDialog = true">
          <IconPlus :size="16" />
          <span>Add Observation</span>
        </Button>
      </div>

      <div
        v-if="isLoading && !hasObservations"
        data-test="loading-container"
        class="flex flex-col items-center justify-center py-8"
      >
        <IconLoader2 class="animate-spin h-8 w-8 mb-2" />
        <span class="text-sm text-muted-foreground">Loading observations...</span>
      </div>

      <Table v-else>
        <TableHeader>
          <TableRow>
            <TableHead>Date</TableHead>
            <TableHead>Health</TableHead>
            <TableHead>Height (cm)</TableHead>
            <TableHead>Notes</TableHead>
            <TableHead class="w-[80px]"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableEmpty v-if="!hasObservations" :colspan="6">
            No observations logged yet.
          </TableEmpty>
          <TableRow v-for="obs in observations?.results" :key="obs.id">
            <TableCell>{{ formatDate(obs.createdAt) }}</TableCell>
            <TableCell>
              <Badge :variant="HEALTH_BADGE_VARIANT[obs.healthStatus]">
                {{ HEALTH_LABEL[obs.healthStatus] }}
              </Badge>
            </TableCell>
            <TableCell>{{ obs.heightCm ?? "—" }}</TableCell>
            <TableCell class="max-w-[120px] truncate">{{ obs.notes || "—" }}</TableCell>
            <TableCell>
              <div class="flex items-center gap-1">
                <Button variant="ghost" size="icon" class="h-8 w-8" @click="setViewDialog(obs)">
                  <IconEye :size="14" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  class="h-8 w-8"
                  @click="setUpdateDialog(obs.id, toObservationForm(obs))"
                >
                  <IconPencil :size="14" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  class="h-8 w-8 text-red-600 hover:text-red-700"
                  @click="confirmDelete(obs.id)"
                >
                  <IconTrash :size="14" />
                </Button>
              </div>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>

      <div v-if="hasObservations" class="flex items-center justify-between gap-4 py-4">
        <div class="text-sm font-medium">
          Page {{ pagination.pageIndex + 1 }} of {{ totalPages }}
        </div>
        <div class="flex items-center gap-1">
          <Button
            size="sm"
            variant="outline"
            :disabled="pagination.pageIndex === 0"
            @click="pagination.pageIndex--"
          >
            Previous
          </Button>
          <Button
            size="sm"
            variant="outline"
            :disabled="pagination.pageIndex + 1 >= totalPages"
            @click="pagination.pageIndex++"
          >
            Next
          </Button>
        </div>
      </div>
    </SheetContent>
  </Sheet>

  <!-- View Dialog -->
  <PlantingDailyObservationViewDialog
    v-if="observationToView"
    v-model:open="openViewDialog"
    :observation="observationToView"
  />

  <!-- Create Dialog -->
  <PlantingDailyObservationCreateDialog
    v-model:open="openCreateDialog"
    :isLoading="isLoading"
    :isCreateSuccess="isCreateSuccess"
    @submit="handleCreate"
  />

  <!-- Update Dialog -->
  <PlantingDailyObservationUpdateDialog
    v-if="observationUpdateFormState"
    v-model:open="openUpdateDialog"
    :id="observationIdToUpdate"
    :observationFormInitialState="observationUpdateFormState"
    :isLoading="isLoading"
    :isUpdateSuccess="isUpdateSuccess"
    @submit="handleUpdate"
  />

  <!-- Delete Confirmation -->
  <AlertDialog :open="isDeleteDialogOpen" @update:open="isDeleteDialogOpen = $event">
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
        <AlertDialogDescription>
          This will permanently delete this observation.
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel>Cancel</AlertDialogCancel>
        <AlertDialogAction @click="handleDelete" class="bg-red-600 hover:bg-red-700">
          Delete
        </AlertDialogAction>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
