<script setup lang="ts">
import { computed, ref } from "vue"
import { RouterLink } from "vue-router"
import AppLayout from "@/layouts/AppLayout.vue"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  Table,
  TableBody,
  TableCell,
  TableEmpty,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { IconGrowth, IconMap2, IconCircleFilled, IconCircleCheck } from "@tabler/icons-vue"
import { usePlantings } from "@/composables/usePlantings"
import { usePlantingLocations } from "@/composables/usePlantingLocations"
import { formatDate } from "@/utils/formatting"

const pagination = ref({ pageIndex: 0, pageSize: 100 })

const { plantings } = usePlantings(pagination)
const { locations } = usePlantingLocations(pagination)

const totalPlantings = computed(() => plantings.value?.count ?? 0)
const totalLocations = computed(() => locations.value?.count ?? 0)

const locationResults = computed(() => locations.value?.results ?? [])

const inUseCount = computed(
  () => locationResults.value.filter((l) => l.currentStatus?.status === "IN_USE").length,
)

const availableCount = computed(
  () =>
    locationResults.value.filter((l) => !l.currentStatus || l.currentStatus.status === "AVAILABLE")
      .length,
)

const recentPlantings = computed(() => {
  const results = [...(plantings.value?.results ?? [])]
  results.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
  return results.slice(0, 5)
})

const LOCATION_TYPE_LABEL: Record<string, string> = {
  NURSERYPOT: "Nursery Pot",
  POT: "Pot",
  GROUND: "Ground",
}

const STATUS_BADGE_VARIANT: Record<string, "secondary" | "default" | "destructive" | "outline"> = {
  AVAILABLE: "secondary",
  IN_USE: "default",
  DAMAGED: "destructive",
  DESTROYED: "destructive",
  RETIRED: "outline",
}

const STATUS_LABEL: Record<string, string> = {
  AVAILABLE: "Available",
  IN_USE: "In Use",
  DAMAGED: "Damaged",
  DESTROYED: "Destroyed",
  RETIRED: "Retired",
}
</script>

<template>
  <AppLayout>
    <div class="space-y-8">
      <!-- Plantings Section -->
      <div class="space-y-4">
        <p
          class="text-xs font-semibold uppercase text-muted-foreground tracking-wide flex items-center gap-1.5"
        >
          <IconGrowth :size="14" />
          Plantings
        </p>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardHeader class="pb-2">
              <CardDescription>Total Plantings</CardDescription>
              <CardTitle class="text-3xl">{{ totalPlantings }}</CardTitle>
            </CardHeader>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <div class="flex items-center justify-between">
              <div>
                <CardTitle>Recent Plantings</CardTitle>
                <CardDescription>The 5 most recently added plantings</CardDescription>
              </div>
              <RouterLink
                to="/plantings"
                class="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                View all
              </RouterLink>
            </div>
          </CardHeader>
          <CardContent class="pt-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Crop</TableHead>
                  <TableHead>Variety</TableHead>
                  <TableHead>Added</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableEmpty v-if="recentPlantings.length === 0" :colspan="3">
                  No plantings yet.
                </TableEmpty>
                <TableRow v-for="planting in recentPlantings" :key="planting.id">
                  <TableCell class="font-medium">{{ planting.cropName }}</TableCell>
                  <TableCell>{{ planting.varietyName }}</TableCell>
                  <TableCell class="text-muted-foreground">
                    {{ formatDate(planting.createdAt) }}
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>

      <!-- Planting Locations Section -->
      <div class="space-y-4">
        <p
          class="text-xs font-semibold uppercase text-muted-foreground tracking-wide flex items-center gap-1.5"
        >
          <IconMap2 :size="14" />
          Planting Locations
        </p>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <Card>
            <CardHeader class="pb-2">
              <CardDescription>Total Locations</CardDescription>
              <CardTitle class="text-3xl">{{ totalLocations }}</CardTitle>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader class="pb-2">
              <CardDescription class="flex items-center gap-1.5">
                <IconCircleFilled :size="14" />
                In Use
              </CardDescription>
              <CardTitle class="text-3xl">{{ inUseCount }}</CardTitle>
            </CardHeader>
          </Card>

          <Card>
            <CardHeader class="pb-2">
              <CardDescription class="flex items-center gap-1.5">
                <IconCircleCheck :size="14" />
                Available
              </CardDescription>
              <CardTitle class="text-3xl">{{ availableCount }}</CardTitle>
            </CardHeader>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <div class="flex items-center justify-between">
              <div>
                <CardTitle>Location Overview</CardTitle>
                <CardDescription>Current status of all planting locations</CardDescription>
              </div>
              <RouterLink
                to="/planting-locations"
                class="text-sm text-muted-foreground hover:text-foreground transition-colors"
              >
                View all
              </RouterLink>
            </div>
          </CardHeader>
          <CardContent class="pt-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                <TableEmpty v-if="locationResults.length === 0" :colspan="3">
                  No locations yet.
                </TableEmpty>
                <TableRow v-for="location in locationResults" :key="location.id">
                  <TableCell class="font-medium">{{ location.name }}</TableCell>
                  <TableCell class="text-muted-foreground">
                    {{ LOCATION_TYPE_LABEL[location.locationType] ?? location.locationType }}
                  </TableCell>
                  <TableCell>
                    <Badge
                      v-if="location.currentStatus"
                      :variant="STATUS_BADGE_VARIANT[location.currentStatus.status] ?? 'outline'"
                    >
                      {{
                        STATUS_LABEL[location.currentStatus.status] ?? location.currentStatus.status
                      }}
                    </Badge>
                    <span v-else class="text-sm text-muted-foreground">No status</span>
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </div>
  </AppLayout>
</template>
