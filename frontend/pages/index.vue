<template>
  <v-container>
    <!-- サマリー -->
    <v-row class="mb-4">
      <v-col cols="6" sm="3">
        <v-card color="grey-lighten-4" variant="flat">
          <v-card-text class="text-center">
            <div class="text-h5">{{ totalCount }}</div>
            <div class="text-caption">全商品</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="red-lighten-5" variant="flat">
          <v-card-text class="text-center">
            <div class="text-h5 text-red">{{ dangerCount }}</div>
            <div class="text-caption">要補充</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="orange-lighten-5" variant="flat">
          <v-card-text class="text-center">
            <div class="text-h5 text-orange">{{ warningCount }}</div>
            <div class="text-caption">注意</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="blue-lighten-5" variant="flat">
          <v-card-text class="text-center">
            <div class="text-h5 text-blue">{{ safeCount }}</div>
            <div class="text-caption">正常</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- フィルタ -->
    <v-row class="mb-2" align="center">
      <v-col cols="12" sm="6">
        <v-btn-toggle v-model="urgencyFilter" color="primary" variant="outlined" divided>
          <v-btn value="">すべて</v-btn>
          <v-btn value="danger" color="red">要補充</v-btn>
          <v-btn value="warning" color="orange">注意</v-btn>
          <v-btn value="safe" color="blue">正常</v-btn>
        </v-btn-toggle>
      </v-col>
      <v-col cols="12" sm="6">
        <v-text-field
          v-model="search"
          prepend-inner-icon="mdi-magnify"
          label="商品名で検索"
          variant="outlined"
          density="compact"
          hide-details
          clearable
        />
      </v-col>
    </v-row>

    <!-- ローディング -->
    <v-row v-if="pending" class="mt-4">
      <v-col class="text-center">
        <v-progress-circular indeterminate color="primary" />
      </v-col>
    </v-row>

    <!-- エラー -->
    <v-alert v-else-if="loadError" type="error" class="mt-4">
      データの取得に失敗しました: {{ loadError }}
    </v-alert>

    <!-- 商品グリッド -->
    <DashboardProductGrid v-else :products="filteredProducts" />
  </v-container>
</template>

<script setup lang="ts">
import type { ProductWithStatus } from '~/types'

const { products, pending, error: productsError } = useProducts()
const { fetchLatestByProductIds } = useDetectionLogs()
const { enrichProducts } = useInventoryStatus()

const urgencyFilter = ref('')
const search = ref('')
const loadError = ref<string | null>(null)

const enrichedProducts = ref<ProductWithStatus[]>([])

watch(products, async (newProducts) => {
  if (!newProducts || newProducts.length === 0) {
    enrichedProducts.value = []
    return
  }

  try {
    const ids = newProducts.map((p) => p.id)
    const latestDetections = await fetchLatestByProductIds(ids)
    enrichedProducts.value = enrichProducts(newProducts, latestDetections)
  } catch (e: any) {
    loadError.value = e.message
  }
}, { immediate: true })

watch(productsError, (err) => {
  if (err) loadError.value = err.message
})

const filteredProducts = computed(() => {
  let result = enrichedProducts.value

  if (urgencyFilter.value) {
    result = result.filter((p) => p.urgency === urgencyFilter.value)
  }

  if (search.value) {
    const q = search.value.toLowerCase()
    result = result.filter((p) => p.name.toLowerCase().includes(q))
  }

  return result
})

const totalCount = computed(() => enrichedProducts.value.length)
const dangerCount = computed(() => enrichedProducts.value.filter((p) => p.urgency === 'danger').length)
const warningCount = computed(() => enrichedProducts.value.filter((p) => p.urgency === 'warning').length)
const safeCount = computed(() => enrichedProducts.value.filter((p) => p.urgency === 'safe').length)
</script>
