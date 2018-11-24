<template>
  <div>
    <h2>Administration</h2>
    <p>Customize Yeti's behavior. Get a glimpse of existing tags, manage Users,
    do other awesome things...</p>
    <nav class="nav nav-pills nav-fill">
      <router-link class="nav-item nav-link" :to="{name: 'Tags'}">Tags</router-link>
      <router-link class="nav-item nav-link" :to="{name: 'Async'}">Async jobs</router-link>
      <router-link class="nav-item nav-link" :to="{name: 'KillChains'}">Kill chains</router-link>
      <a class="nav-item nav-link disabled" href="#">Users</a>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
}
</script>

<style lang="css">
</style>
