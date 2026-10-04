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
import FertilizerLogCreateDialog from "./FertilizerLogCreateDialog.vue"
import FertilizerLogUpdateDialog from "./FertilizerLogUpdateDialog.vue"
import FertilizerLogViewDialog from "./FertilizerLogViewDialog.vue"
import { useFertilizerLogs } from "@/composables/useFertilizerLogs"
import type { FertilizerLog } from "@/types/fertilizerLog"
import type { Fertilizer } from "@/types/fertilizer"
import type { FertilizerLogForm } from "@/schemas/fertilizerLog.schemas"
import { formatDate } from "@/utils/formatting"
import { EVENT_TYPE_LABEL } from "./constants"

const open = defineModel<boolean>("open")
const { fertilizerId, fertilizer } = defineProps<{
  fertilizerId: number
  fertilizer: Fertilizer
}>()

const pagination = ref({ pageIndex: 0, pageSize: 10 })

const { logs, isLoading, isCreateSuccess, isUpdateSuccess, createLog, updateLog, deleteLog } =
  useFertilizerLogs(
    toRef(() => fertilizerId),
    pagination,
  )

const totalPages = computed(() => Math.ceil((logs.value?.count ?? 0) / pagination.value.pageSize))

// Create dialog
const openCreateDialog = ref<boolean>(false)

// Update dialog
const openUpdateDialog = ref<boolean>(false)
const logIdToUpdate = ref<number>(0)
const logUpdateFormState = ref<FertilizerLogForm | null>(null)

// View dialog
const openViewDialog = ref<boolean>(false)
const logToView = ref<FertilizerLog | null>(null)

// Delete dialog
const isDeleteDialogOpen = ref<boolean>(false)
const logIdToDelete = ref<number>(0)

const setViewDialog = (entry: FertilizerLog): void => {
  logToView.value = entry
  openViewDialog.value = true
}

const setUpdateDialog = (entry: FertilizerLog): void => {
  logIdToUpdate.value = entry.id
  logUpdateFormState.value = toLogForm(entry)
  openUpdateDialog.value = true
}

const confirmDelete = (id: number): void => {
  logIdToDelete.value = id
  isDeleteDialogOpen.value = true
}

const handleCreate = async (
  payload: FertilizerLogForm,
  onError: (err: unknown) => void,
): Promise<void> => {
  try {
    await createLog(payload)
    pagination.value.pageIndex = 0
  } catch (err) {
    onError(err)
  }
}

const handleUpdate = async (
  id: number,
  payload: FertilizerLogForm,
  onError: (err: unknown) => void,
): Promise<void> => {
  try {
    await updateLog({ id, payload })
  } catch (err) {
    onError(err)
  }
}

const handleDelete = async (): Promise<void> => {
  await deleteLog(logIdToDelete.value)
  isDeleteDialogOpen.value = false
  pagination.value.pageIndex = 0
}

const toLogForm = (entry: FertilizerLog): FertilizerLogForm => ({
  logDate: entry.logDate,
  eventType: entry.eventType,
  itemAdded: entry.itemAdded ?? "",
  quantity: entry.quantity ?? "",
  notes: entry.notes ?? "",
})

const hasLogs = computed(() => (logs.value?.results?.length ?? 0) > 0)
</script>

<template>
  <Sheet v-model:open="open">
    <SheetContent class="sm:max-w-lg w-full flex flex-col gap-4 px-4">
      <SheetHeader>
        <SheetTitle>Logs: {{ fertilizer.name }}</SheetTitle>
        <SheetDescription
          >Keep track of what's been added to this fertilizer over time.</SheetDescription
        >
      </SheetHeader>

      <div class="flex justify-end">
        <Button variant="outline" size="sm" @click="openCreateDialog = true">
          <IconPlus :size="16" />
          <span>Add Entry</span>
        </Button>
      </div>

      <div
        v-if="isLoading && !hasLogs"
        data-test="loading-container"
        class="flex flex-col items-center justify-center py-8"
      >
        <IconLoader2 class="animate-spin h-8 w-8 mb-2" />
        <span class="text-sm text-muted-foreground">Loading logs...</span>
      </div>

      <Table v-else>
        <TableHeader>
          <TableRow>
            <TableHead>Date</TableHead>
            <TableHead>Event</TableHead>
            <TableHead>Item</TableHead>
            <TableHead class="w-[96px]"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableEmpty v-if="!hasLogs" :colspan="4"> No logs recorded yet. </TableEmpty>
          <TableRow v-for="entry in logs?.results" :key="entry.id">
            <TableCell>{{ formatDate(entry.logDate) }}</TableCell>
            <TableCell>
              <Badge variant="secondary">
                {{ EVENT_TYPE_LABEL[entry.eventType] ?? entry.eventType }}
              </Badge>
            </TableCell>
            <TableCell class="max-w-[140px] truncate">
              {{ entry.itemAdded || "—" }}
            </TableCell>
            <TableCell>
              <div class="flex items-center gap-1">
                <Button variant="ghost" size="icon" class="h-8 w-8" @click="setViewDialog(entry)">
                  <IconEye :size="14" />
                </Button>
                <Button variant="ghost" size="icon" class="h-8 w-8" @click="setUpdateDialog(entry)">
                  <IconPencil :size="14" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  class="h-8 w-8 text-red-600 hover:text-red-700"
                  @click="confirmDelete(entry.id)"
                >
                  <IconTrash :size="14" />
                </Button>
              </div>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>

      <div v-if="hasLogs" class="flex items-center justify-between gap-4 py-4">
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
  <FertilizerLogViewDialog v-if="logToView" v-model:open="openViewDialog" :log="logToView" />

  <!-- Create Dialog -->
  <FertilizerLogCreateDialog
    v-model:open="openCreateDialog"
    :fertilizerName="fertilizer.name"
    :isLoading="isLoading"
    :isCreateSuccess="isCreateSuccess"
    @submit="handleCreate"
  />

  <!-- Update Dialog -->
  <FertilizerLogUpdateDialog
    v-if="logUpdateFormState"
    v-model:open="openUpdateDialog"
    :id="logIdToUpdate"
    :logFormInitialState="logUpdateFormState"
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
          This will permanently delete this log entry.
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
