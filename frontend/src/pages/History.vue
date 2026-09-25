<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
// 旧 run 未存贴向时按竖贴展示(改造前均为竖贴);新 run 展示写入时钉住的贴向
const orientLabel = (r) => r.result?.orientation === 'horizontal' ? '横贴' : '竖贴'
</script>
<template>
  <div class="page"><h1>记录</h1><ul><li v-for="r in items" :key="r.id">{{ r.wall_name }} → {{ r.result?.rolls }} 卷 · {{ orientLabel(r) }} · {{ r.result?.drops }} 条</li></ul></div>
</template>
