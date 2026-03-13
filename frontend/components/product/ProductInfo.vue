<template>
  <v-card>
    <v-img
      v-if="product.image_url"
      :src="product.image_url"
      height="200"
      cover
    />
    <div v-else class="image-placeholder d-flex align-center justify-center">
      <v-icon size="64" color="grey-lighten-1">mdi-package-variant</v-icon>
    </div>

    <v-card-title class="d-flex align-center justify-space-between">
      {{ product.name }}
      <DashboardUrgencyBadge :urgency="product.urgency" />
    </v-card-title>

    <v-card-text>
      <v-list density="compact">
        <v-list-item>
          <template #prepend>
            <v-icon>mdi-store</v-icon>
          </template>
          <v-list-item-title>店頭</v-list-item-title>
          <v-list-item-subtitle>
            {{ product.shelfCount }} / {{ product.shelf_max }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item>
          <template #prepend>
            <v-icon>mdi-warehouse</v-icon>
          </template>
          <v-list-item-title>在庫（裏）</v-list-item-title>
          <v-list-item-subtitle>
            {{ product.stock_count }} / {{ product.stock_max }}
          </v-list-item-subtitle>
        </v-list-item>

        <v-list-item v-if="product.replenishCount > 0">
          <template #prepend>
            <v-icon color="red">mdi-alert-circle</v-icon>
          </template>
          <v-list-item-title class="text-red font-weight-bold">
            補充が必要: {{ product.replenishCount }} 個
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import type { ProductWithStatus } from '~/types'

defineProps<{
  product: ProductWithStatus
}>()
</script>

<style scoped>
.image-placeholder {
  height: 200px;
  background-color: #f5f5f5;
}
</style>
