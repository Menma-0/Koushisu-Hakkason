<template>
  <v-card>
    <v-card-title>
      <v-icon class="mr-2">mdi-history</v-icon>
      検知履歴
    </v-card-title>

    <v-card-text v-if="logs.length === 0">
      <v-alert type="info" variant="tonal">
        検知データがありません
      </v-alert>
    </v-card-text>

    <v-table v-else density="comfortable">
      <thead>
        <tr>
          <th>検知日時</th>
          <th class="text-right">店頭個数</th>
          <th>画像</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in logs" :key="log.id">
          <td>{{ formatDate(log.detected_at) }}</td>
          <td class="text-right font-weight-bold">{{ log.shelf_count }}</td>
          <td>
            <v-btn
              v-if="log.image_url"
              :href="log.image_url"
              target="_blank"
              variant="text"
              size="small"
              icon="mdi-image"
            />
            <span v-else class="text-grey">-</span>
          </td>
        </tr>
      </tbody>
    </v-table>
  </v-card>
</template>

<script setup lang="ts">
import type { DetectionLog } from '~/types'

defineProps<{
  logs: DetectionLog[]
}>()

const formatDate = (iso: string): string => {
  const d = new Date(iso)
  return d.toLocaleString('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>
