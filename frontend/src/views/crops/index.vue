<script setup lang="ts">
import AppLayout from "@/layouts/AppLayout.vue"
import CropsTable from "@/components/CropsTable.vue"
import { Button } from "@/components/ui/button"
import { IconPlus } from "@tabler/icons-vue"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Label } from "@/components/ui/label"

const data = [
  {
    name: "Tomato",
    scientific_name: "Solanum lycopersicum",
    category: "VEGETABLE",
    sunlight_requirement: "FULL SUN",
    min_days_to_harvest: 60,
    max_days_to_harvest: 90,
  },
  {
    name: "Lettuce",
    scientific_name: "Lactuca sativa",
    category: "VEGETABLE",
    sunlight_requirement: "PARTIAL SHADE",
    min_days_to_harvest: 30,
    max_days_to_harvest: 50,
  },
  {
    name: "Carrot",
    scientific_name: "Daucus carota",
    category: "VEGETABLE",
    sunlight_requirement: "FULL SUN",
    min_days_to_harvest: 70,
    max_days_to_harvest: 80,
  },
  {
    name: "Cucumber",
    scientific_name: "Cucumis sativus",
    category: "VEGETABLE",
    sunlight_requirement: "FULL SUN",
    min_days_to_harvest: 50,
    max_days_to_harvest: 70,
  },
  {
    name: "Basil",
    scientific_name: "Ocimum basilicum",
    category: "HERB",
    sunlight_requirement: "FULL SUN",
    min_days_to_harvest: 40,
    max_days_to_harvest: 60,
  },
  {
    name: "Strawberry",
    scientific_name: "Fragaria × ananassa",
    category: "FRUIT",
    sunlight_requirement: "FULL SUN",
    min_days_to_harvest: 90,
    max_days_to_harvest: 120,
  },
  {
    name: "Spinach",
    scientific_name: "Spinacia oleracea",
    category: "VEGETABLE",
    sunlight_requirement: "PARTIAL SHADE",
    min_days_to_harvest: 35,
    max_days_to_harvest: 45,
  },
  {
    name: "Bell Pepper",
    scientific_name: "Capsicum annuum",
    category: "VEGETABLE",
    sunlight_requirement: "FULL SUN",
    min_days_to_harvest: 60,
    max_days_to_harvest: 80,
  },
  {
    name: "Rosemary",
    scientific_name: "Salvia rosmarinus",
    category: "HERB",
    sunlight_requirement: "FULL SUN",
    min_days_to_harvest: 90,
    max_days_to_harvest: 120,
  },
  {
    name: "Blueberry",
    scientific_name: "Vaccinium corymbosum",
    category: "FRUIT",
    sunlight_requirement: "FULL SUN",
    min_days_to_harvest: 120,
    max_days_to_harvest: 150,
  },
]
</script>

<template>
  <AppLayout>
    <div class="flex justify-end w-full">
      <Button variant="outline" size="sm">
        <IconPlus />
        <span class="hidden lg:inline">Add Crop</span>
      </Button>
    </div>
    <CropsTable :data="data" />
  </AppLayout>
</template>
