<script setup>
defineProps({ drops: Number, dropLen: Number, rolls: Number, orientation: String })
</script>
<template>
  <div class="strip-bar" :class="{ horizontal: orientation === 'horizontal' }">
    <template v-if="orientation === 'horizontal'">
      <div v-for="n in Math.min(drops || 0, 24)" :key="n" class="strip" :style="{ width: `${Math.min(240, (dropLen || 2) * 15)}px` }"></div>
    </template>
    <template v-else>
      <div v-for="n in Math.min(drops || 0, 24)" :key="n" class="strip" :style="{ height: `${Math.min(120, (dropLen || 2) * 30)}px` }"></div>
    </template>
    <p>共 {{ drops }} 条，约 {{ rolls }} 卷</p>
  </div>
</template>
