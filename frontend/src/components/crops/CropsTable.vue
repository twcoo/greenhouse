<script setup lang="ts">
import BaseDataTable from "@/components/BaseDataTable.vue"
import { Crop } from "@/types/crop"
import { columns } from "./CropsColumns"

defineProps<{
  data: Crop[]
}>()
</script>

<template>
  <BaseDataTable
    :data="data"
    :columns="columns"
    :filterableColumns="['category', 'sunlight_requirement']"
  />
</template>
