<script setup lang="ts">
import { ref } from "vue"
import { MoreHorizontal } from "lucide-vue-next"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
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
import type { Planting } from "@/types/planting"
import type { TableRowProps } from "@/types/table"

const { row, table } = defineProps<TableRowProps<Planting>>()

const isDeleteDialogOpen = ref<boolean>(false)

const handleUpdate = async (id: number, planting: Planting): Promise<void> => {
  await table.options.meta?.update(id, planting)
}

const handleManageLocations = (): void => {
  table.options.meta?.action?.("manage-locations", row.original.id)
}

const handleDailyObservations = (): void => {
  table.options.meta?.action?.("daily-observations", row.original.id)
}

const handleDelete = (): void => {
  isDeleteDialogOpen.value = true
}

const confirmDelete = async (id: number): Promise<void> => {
  await table.options.meta?.delete(id)
}
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="ghost" class="h-8 w-8 p-0">
        <MoreHorizontal class="h-4 w-4" />
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end">
      <DropdownMenuLabel>Actions</DropdownMenuLabel>
      <DropdownMenuItem @click="handleUpdate(row.original.id, row.original)">
        Update
      </DropdownMenuItem>
      <DropdownMenuItem @click="handleManageLocations"> Manage Locations </DropdownMenuItem>
      <DropdownMenuItem @click="handleDailyObservations"> Daily Observations </DropdownMenuItem>
      <DropdownMenuSeparator />
      <DropdownMenuItem @click="handleDelete">Delete</DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>

  <AlertDialog :open="isDeleteDialogOpen" @update:open="isDeleteDialogOpen = $event">
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
        <AlertDialogDescription>
          This action cannot be undone. This will permanently delete the planting record of
          <span class="font-semibold text-foreground">{{ row.original.varietyName }}</span>
          ({{ row.original.cropName }}).
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel>Cancel</AlertDialogCancel>
        <AlertDialogAction
          @click="confirmDelete(row.original.id)"
          class="bg-red-600 hover:bg-red-700"
        >
          Delete
        </AlertDialogAction>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
