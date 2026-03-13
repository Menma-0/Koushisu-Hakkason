<template>
  <v-card>
    <v-card-title>
      <v-icon class="mr-2">mdi-pencil</v-icon>
      在庫数の更新（手入力）
    </v-card-title>

    <v-card-text>
      <v-text-field
        v-model.number="stockValue"
        type="number"
        label="現在の在庫数（裏）"
        :min="0"
        :max="maxCount"
        :rules="rules"
        variant="outlined"
        class="mb-2"
      />

      <v-btn
        color="primary"
        :loading="saving"
        :disabled="!isValid"
        block
        @click="save"
      >
        更新する
      </v-btn>
    </v-card-text>

    <v-snackbar v-model="showSuccess" color="success" :timeout="2000">
      在庫数を更新しました
    </v-snackbar>

    <v-snackbar v-model="showError" color="error" :timeout="3000">
      {{ errorMessage }}
    </v-snackbar>
  </v-card>
</template>

<script setup lang="ts">
const props = defineProps<{
  productId: string
  currentCount: number
  maxCount: number
}>()

const emit = defineEmits<{
  updated: []
}>()

const { updateStockCount } = useProducts()

const stockValue = ref(props.currentCount)
const saving = ref(false)
const showSuccess = ref(false)
const showError = ref(false)
const errorMessage = ref('')

watch(() => props.currentCount, (val) => {
  stockValue.value = val
})

const rules = [
  (v: number) => v >= 0 || '0以上の値を入力してください',
  (v: number) => v <= props.maxCount || `${props.maxCount}以下の値を入力してください`,
]

const isValid = computed(() =>
  stockValue.value >= 0 && stockValue.value <= props.maxCount
)

const save = async () => {
  if (!isValid.value) return

  saving.value = true
  try {
    await updateStockCount({
      id: props.productId,
      stock_count: stockValue.value,
    })
    showSuccess.value = true
    emit('updated')
  } catch (e: any) {
    errorMessage.value = e.message || '更新に失敗しました'
    showError.value = true
  } finally {
    saving.value = false
  }
}
</script>
