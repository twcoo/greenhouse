<script setup lang="ts">
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

interface RowProps {
  row: {
    original: any
  }
}

const props = defineProps<RowProps>()

const handleUpdate = (id: number) => {
  console.log(id)
}

const handleDelete = (id: number) => {
  console.log(id)
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
      <DropdownMenuItem @click="handleUpdate(props.row.original.id)"> Update </DropdownMenuItem>
      <DropdownMenuSeparator />
      <DropdownMenuItem @click="handleDelete(props.row.original.id)">Delete</DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
