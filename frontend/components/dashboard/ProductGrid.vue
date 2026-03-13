<template>
  <v-container>
    <v-row v-if="products.length > 0">
      <v-col
        v-for="product in products"
        :key="product.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <ProductCard :product="product" />
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col>
        <v-alert type="info" variant="tonal">
          商品が登録されていません
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import type { ProductWithStatus } from '~/types'

defineProps<{
  products: ProductWithStatus[]
}>()
</script>
