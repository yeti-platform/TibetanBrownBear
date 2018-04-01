<template lang="html">
  <nav class="col-md-2 d-none d-md-block bg-light sidebar">
    <div class="sidebar-sticky">
      <ul class="nav flex-column">
        <li class="nav-item">
          <router-link class="nav-link" to="/observables">
            <span data-feather="home"></span>Observables
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/entities">
            <span data-feather="file"></span>Entities
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/indicators">
            <span data-feather="file"></span>Indicators
          </router-link>
        </li>
      </ul>

      <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
        <span>Advanced</span>
        <a class="d-flex align-items-center text-muted" href="#">
          <span data-feather="plus-circle"></span>
        </a>
      </h6>
      <ul class="nav flex-column mb-2">
        <li class="nav-item">
          <a class="nav-link" href="#">
            <span data-feather="file-text"></span>
            Browse
          </a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
}
</script>

<style lang="css">
</style>
