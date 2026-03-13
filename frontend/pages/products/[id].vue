<template>
  <v-container>
    <v-btn
      variant="text"
      prepend-icon="mdi-arrow-left"
      class="mb-4"
      @click="navigateTo('/')"
    >
      ダッシュボードに戻る
    </v-btn>

    <!-- ローディング -->
    <v-row v-if="loading" class="mt-4">
      <v-col class="text-center">
        <v-progress-circular indeterminate color="primary" />
      </v-col>
    </v-row>

    <!-- エラー -->
    <v-alert v-else-if="loadError" type="error" class="mt-4">
      {{ loadError }}
    </v-alert>

    <!-- メインコンテンツ -->
    <template v-else-if="enrichedProduct">
      <v-row>
        <v-col cols="12" md="5">
          <ProductProductInfo :product="enrichedProduct" />
        </v-col>
        <v-col cols="12" md="7">
          <ProductStockEditor
            :product-id="enrichedProduct.id"
            :current-count="enrichedProduct.stock_count"
            :max-count="enrichedProduct.stock_max"
            @updated="refreshAll"
          />
        </v-col>
      </v-row>

      <v-row class="mt-4">
        <v-col>
          <ProductDetectionHistory :logs="detectionLogs" />
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

<script setup lang="ts">
import type { Product, DetectionLog, ProductWithStatus } from '~/types'

const route = useRoute()
const productId = route.params.id as string

const { fetchProduct } = useProducts()
const { fetchByProductId, fetchLatestByProductIds } = useDetectionLogs()
const { enrichProduct } = useInventoryStatus()

const product = ref<Product | null>(null)
const detectionLogs = ref<DetectionLog[]>([])
const enrichedProduct = ref<ProductWithStatus | null>(null)
const loading = ref(true)
const loadError = ref<string | null>(null)

const loadData = async () => {
  loading.value = true
  loadError.value = null

  try {
    const [p, logs] = await Promise.all([
      fetchProduct(productId),
      fetchByProductId(productId),
    ])

    if (!p) {
      loadError.value = '商品が見つかりません'
      return
    }

    product.value = p
    detectionLogs.value = logs

    const latestLog = logs.length > 0 ? logs[0] : null
    enrichedProduct.value = enrichProduct(p, latestLog)
  } catch (e: any) {
    loadError.value = e.message || 'データの取得に失敗しました'
  } finally {
    loading.value = false
  }
}

const refreshAll = async () => {
  await loadData()
}

await loadData()
</script>
