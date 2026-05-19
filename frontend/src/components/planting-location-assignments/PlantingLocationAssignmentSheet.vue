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
import { Button } from "@/components/ui/button"
import { IconLoader2, IconPencil, IconPlus, IconTrash } from "@tabler/icons-vue"
import PlantingLocationAssignmentCreateDialog from "./PlantingLocationAssignmentCreateDialog.vue"
import PlantingLocationAssignmentUpdateDialog from "./PlantingLocationAssignmentUpdateDialog.vue"
import { usePlantingLocationAssignments } from "@/composables/usePlantingLocationAssignments"
import type { PlantingLocationAssignmentPayload } from "@/types/plantingLocationAssignment"
import type { PlantingLocationAssignmentForm } from "@/schemas/plantingLocationAssignment.schemas"
import { formatDate } from "@/utils/formatting"

const open = defineModel<boolean>("open")
const { plantingId } = defineProps<{ plantingId: number }>()

const {
  assignments,
  isLoading,
  isCreateSuccess,
  isUpdateSuccess,
  createAssignment,
  updateAssignment,
  deleteAssignment,
} = usePlantingLocationAssignments(toRef(() => plantingId))

// Create dialog
const openCreateDialog = ref<boolean>(false)

// Update dialog
const openUpdateDialog = ref<boolean>(false)
const assignmentIdToUpdate = ref<number>(0)
const assignmentUpdateFormState = ref<PlantingLocationAssignmentForm | null>(null)

// Delete dialog
const isDeleteDialogOpen = ref<boolean>(false)
const assignmentIdToDelete = ref<number>(0)

const setUpdateDialog = (id: number, form: PlantingLocationAssignmentForm): void => {
  assignmentIdToUpdate.value = id
  assignmentUpdateFormState.value = form
  openUpdateDialog.value = true
}

const confirmDelete = (id: number): void => {
  assignmentIdToDelete.value = id
  isDeleteDialogOpen.value = true
}

const handleCreate = async (
  payload: PlantingLocationAssignmentPayload,
  onError: (err: unknown) => void,
): Promise<void> => {
  try {
    await createAssignment(payload)
  } catch (err) {
    onError(err)
  }
}

const handleUpdate = async (
  id: number,
  payload: PlantingLocationAssignmentPayload,
  onError: (err: unknown) => void,
): Promise<void> => {
  try {
    await updateAssignment({ id, payload })
  } catch (err) {
    onError(err)
  }
}

const handleDelete = async (): Promise<void> => {
  await deleteAssignment(assignmentIdToDelete.value)
  isDeleteDialogOpen.value = false
}

const toAssignmentForm = (assignment: {
  plantingLocation: number
  startDate: string
  endDate: string | null
}): PlantingLocationAssignmentForm => ({
  plantingLocation: assignment.plantingLocation,
  startDate: assignment.startDate,
  endDate: assignment.endDate ?? undefined,
})

const hasAssignments = computed(() => (assignments.value?.results?.length ?? 0) > 0)

const isCurrentlyAssigned = computed(
  () => assignments.value?.results?.some((a) => a.endDate === null) ?? false,
)
</script>

<template>
  <Sheet v-model:open="open">
    <SheetContent class="sm:max-w-lg w-full flex flex-col gap-4">
      <SheetHeader>
        <SheetTitle>Location Assignments</SheetTitle>
        <SheetDescription> Manage the location history for this planting. </SheetDescription>
      </SheetHeader>

      <div class="flex flex-col gap-2">
        <p v-if="isCurrentlyAssigned" class="text-sm text-muted-foreground text-center">
          This planting is currently located somewhere. End the active assignment before adding a
          new one.
        </p>
        <div class="flex justify-end">
          <Button
            variant="outline"
            size="sm"
            :disabled="isCurrentlyAssigned"
            @click="openCreateDialog = true"
          >
            <IconPlus :size="16" />
            <span>Add Assignment</span>
          </Button>
        </div>
      </div>

      <div
        v-if="isLoading && !hasAssignments"
        data-test="loading-container"
        class="flex flex-col items-center justify-center py-8"
      >
        <IconLoader2 class="animate-spin h-8 w-8 mb-2" />
        <span class="text-sm text-muted-foreground">Loading assignments...</span>
      </div>

      <Table v-else>
        <TableHeader>
          <TableRow>
            <TableHead>Location</TableHead>
            <TableHead>Start</TableHead>
            <TableHead>End</TableHead>
            <TableHead class="w-[80px]"></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableEmpty v-if="!hasAssignments" :colspan="4">
            No location assignments yet.
          </TableEmpty>
          <TableRow v-for="assignment in assignments?.results" :key="assignment.id">
            <TableCell>{{ assignment.plantingLocationName }}</TableCell>
            <TableCell>{{ formatDate(assignment.startDate) }}</TableCell>
            <TableCell>{{ formatDate(assignment.endDate, "Present") }}</TableCell>
            <TableCell>
              <div class="flex items-center gap-1">
                <Button
                  variant="ghost"
                  size="icon"
                  class="h-8 w-8"
                  @click="setUpdateDialog(assignment.id, toAssignmentForm(assignment))"
                >
                  <IconPencil :size="14" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  class="h-8 w-8 text-red-600 hover:text-red-700"
                  @click="confirmDelete(assignment.id)"
                >
                  <IconTrash :size="14" />
                </Button>
              </div>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </SheetContent>
  </Sheet>

  <!-- Create Dialog -->
  <PlantingLocationAssignmentCreateDialog
    v-model:open="openCreateDialog"
    :isLoading="isLoading"
    :isCreateSuccess="isCreateSuccess"
    @submit="handleCreate"
  />

  <!-- Update Dialog -->
  <PlantingLocationAssignmentUpdateDialog
    v-if="assignmentUpdateFormState"
    v-model:open="openUpdateDialog"
    :id="assignmentIdToUpdate"
    :assignmentFormInitialState="assignmentUpdateFormState"
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
          This will permanently delete this location assignment.
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
