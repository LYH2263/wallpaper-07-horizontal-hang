<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const s = ref({})
const defaultOrientation = ref('vertical')
onMounted(async () => {
  s.value = await getJSON('/api/settings')
  if (s.value.default_orientation) defaultOrientation.value = s.value.default_orientation
})
async function save() {
  s.value = await putJSON(`/api/settings/default_orientation`, { value: defaultOrientation.value })
}
</script>
<template>
  <div class="page"><h1>设置</h1>
    <label>默认贴向
      <select v-model="defaultOrientation">
        <option value="vertical">竖贴</option>
        <option value="horizontal">横贴</option>
      </select>
    </label>
    <button @click="save">保存</button>
    <pre>{{ s }}</pre>
  </div>
</template>
