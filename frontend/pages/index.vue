<template>
  <div class="container">
    <h1>VIS App</h1>
    <p>Backend status: {{ health?.status ?? 'loading...' }}</p>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()

const { data: health } = await useFetch<{ status: string }>(
  `${config.public.apiBase}/health`
)
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  font-family: sans-serif;
}
</style>
