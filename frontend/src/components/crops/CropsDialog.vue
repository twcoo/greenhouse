<script setup lang="ts">
import { computed, reactive } from "vue"
import { Button } from "@/components/ui/button"
import { IconPlus } from "@tabler/icons-vue"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { cropsSchema, type cropsForm } from "@/schemas/crops.schema"

const props = defineProps<{
  mode: "create" | "edit"
}>()

const actionLabel = computed(() => (props.mode === "create" ? "Add" : "Update"))

const form = reactive<cropsForm>({
  name: "",
  scientificName: "",
  category: "",
  sunlightRequirement: "",
  minDaysToHarvest: 0,
  maxDaysToHarvest: 0,
})

async function handleSubmit(): Promise<void> {
  // errors.value = {}
  //
  // const result = cropsSchema.safeParse(form)
  //
  // if (!result.success) {
  //   errors.value = zodToFormErrors(result.error)
  //   return
  // }
  //
  // // await authStore.login(result.data)
}
</script>

<template>
  <Dialog>
    <form @submit.prevent="handleSubmit">
      <DialogTrigger as-child>
        <Button variant="outline">
          <IconPlus />
          <span class="hidden lg:inline">{{ actionLabel }} Crop</span>
        </Button>
      </DialogTrigger>
      <DialogContent class="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{{ actionLabel }} Crop</DialogTitle>
          <DialogDescription>
            {{
              mode === "create"
                ? "Add a new crop to your list. Fill in the details below."
                : "Update the details of this crop. Click save when you're done."
            }}
          </DialogDescription>
        </DialogHeader>
        <div class="grid gap-4">
          <div class="grid gap-3">
            <Label for="name">Name</Label>
            <Input v-model="form.name" id="name" name="name" />
          </div>
          <div class="grid gap-3">
            <Label for="scientificName">Scientific Name</Label>
            <Input v-model="form.scientifiName" id="scientificName" name="scientificName" />
          </div>
          <div class="grid gap-3">
            <Label for="category">Category</Label>
            <Select id="category" v-model="form.category">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="vegetable"> Vegetable </SelectItem>
                <SelectItem value="fruit"> Fruit </SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div class="grid gap-3">
            <Label for="sunlightRequirement">Sunlight Requirement</Label>
            <Select id="sunlightRequirement" v-model="form.sunlightRequirement">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select sunlight requirement" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="FULL SUN"> Full Sun </SelectItem>
                <SelectItem value="PART SUN"> Partial Sun </SelectItem>
                <SelectItem value="FULL SHADE"> Full Shade </SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div class="grid gap-3">
            <Label for="minDaysToHarvest">Min Days To Harvest</Label>
            <Input type="number" id="minDaysToHarvest" name="minDaysToHarvest" />
          </div>
          <div class="grid gap-3">
            <Label for="maxDaysToHarvest">Max Days To Harvest</Label>
            <Input type="number" id="maxDaysToHarvest" name="maxDaysToHarvest" />
          </div>
        </div>
        <DialogFooter>
          <DialogClose as-child>
            <Button variant="outline"> Cancel </Button>
          </DialogClose>
          <Button type="submit"> Save </Button>
        </DialogFooter>
      </DialogContent>
    </form>
  </Dialog>
</template>
