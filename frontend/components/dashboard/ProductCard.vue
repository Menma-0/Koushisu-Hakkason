<template>
  <v-card class="product-card" @click="navigateTo(`/products/${product.id}`)">
    <v-img
      v-if="product.image_url"
      :src="product.image_url"
      height="140"
      cover
    />
    <div v-else class="image-placeholder d-flex align-center justify-center">
      <v-icon size="48" color="grey-lighten-1">mdi-package-variant</v-icon>
    </div>

    <v-card-title class="d-flex align-center justify-space-between">
      <span class="text-truncate">{{ product.name }}</span>
      <UrgencyBadge :urgency="product.urgency" />
    </v-card-title>

    <v-card-text>
      <div class="d-flex justify-space-between mb-1">
        <span class="text-body-2">店頭</span>
        <span class="text-body-2 font-weight-bold">
          {{ product.shelfCount }} / {{ product.shelf_max }}
        </span>
      </div>
      <v-progress-linear
        :model-value="shelfPercent"
        :color="shelfBarColor"
        height="8"
        rounded
        class="mb-3"
      />

      <div class="d-flex justify-space-between mb-1">
        <span class="text-body-2">在庫（裏）</span>
        <span class="text-body-2 font-weight-bold">
          {{ product.stock_count }} / {{ product.stock_max }}
        </span>
      </div>
      <v-progress-linear
        :model-value="stockPercent"
        :color="stockBarColor"
        height="8"
        rounded
        class="mb-3"
      />

      <div v-if="product.replenishCount > 0" class="text-center">
        <v-chip color="red" variant="outlined" size="small">
          補充: {{ product.replenishCount }} 個
        </v-chip>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import type { ProductWithStatus } from '~/types'

const props = defineProps<{
  product: ProductWithStatus
}>()

const shelfPercent = computed(() =>
  props.product.shelf_max > 0
    ? (props.product.shelfCount / props.product.shelf_max) * 100
    : 0
)

const stockPercent = computed(() =>
  props.product.stock_max > 0
    ? (props.product.stock_count / props.product.stock_max) * 100
    : 0
)

const shelfBarColor = computed(() =>
  shelfPercent.value < 20 ? 'red' : shelfPercent.value < 50 ? 'orange' : 'blue'
)

const stockBarColor = computed(() =>
  stockPercent.value < 20 ? 'red' : stockPercent.value < 50 ? 'orange' : 'blue'
)
</script>

<style scoped>
.product-card {
  cursor: pointer;
  transition: transform 0.15s;
}
.product-card:hover {
  transform: translateY(-2px);
}
.image-placeholder {
  height: 140px;
  background-color: #f5f5f5;
}
</style>
