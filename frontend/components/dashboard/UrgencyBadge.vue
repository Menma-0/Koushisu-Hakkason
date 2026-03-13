<template>
  <v-chip :color="color" size="small" label>
    {{ label }}
  </v-chip>
</template>

<script setup lang="ts">
import type { UrgencyLevel } from '~/types'

const props = defineProps<{
  urgency: UrgencyLevel
}>()

const { urgencyColor, urgencyLabel } = useInventoryStatus()

const color = computed(() => urgencyColor(props.urgency))
const label = computed(() => urgencyLabel(props.urgency))
</script>
