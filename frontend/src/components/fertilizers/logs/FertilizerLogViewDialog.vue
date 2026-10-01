<script setup lang="ts">
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import { formatDate } from "@/utils/formatting"
import type { FertilizerLog } from "@/types/fertilizerLog"
import { EVENT_TYPE_LABEL } from "./constants"

const open = defineModel<boolean>("open")
const { log } = defineProps<{ log: FertilizerLog | null }>()
</script>

<template>
  <Dialog v-model:open="open">
    <DialogContent class="sm:max-w-[500px]">
      <DialogHeader>
        <DialogTitle>Log Entry Details</DialogTitle>
        <DialogDescription v-if="log"> Logged on {{ formatDate(log.logDate) }} </DialogDescription>
      </DialogHeader>

      <div v-if="log" class="space-y-4">
        <div class="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1.5 text-sm">
          <span class="text-muted-foreground">Event Type</span>
          <span>
            <Badge variant="secondary">
              {{ EVENT_TYPE_LABEL[log.eventType] ?? log.eventType }}
            </Badge>
          </span>
          <template v-if="log.itemAdded">
            <span class="text-muted-foreground">Item Added</span>
            <span>{{ log.itemAdded }}</span>
          </template>
          <template v-if="log.quantity">
            <span class="text-muted-foreground">Quantity</span>
            <span>{{ log.quantity }}</span>
          </template>
        </div>

        <div v-if="log.notes">
          <div class="flex items-center gap-2">
            <span class="text-xs font-semibold uppercase tracking-wider text-muted-foreground"
              >Notes</span
            >
            <div class="flex-1 h-px bg-border" />
          </div>
          <p class="text-sm mt-2">{{ log.notes }}</p>
        </div>
      </div>
    </DialogContent>
  </Dialog>
</template>
