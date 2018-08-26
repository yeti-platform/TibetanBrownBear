<template lang="html">
  <nav class="col-md-2 d-none d-md-block bg-light sidebar">
    <div class="sidebar-sticky">
      <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
        <span>Intelligence</span>
        <a class="d-flex align-items-center text-muted" href="#">
          <span data-feather="plus-circle"></span>
        </a>
      </h6>
      <ul class="nav flex-column">
        <li class="nav-item">

        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'malware'}}">
            <span data-feather="file"></span>Malware
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'threat-actor'}}">
            <span data-feather="file"></span>Actors
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'attack-pattern'}}">
            <span data-feather="file"></span>Attack Patterns (TTPs)
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'tool'}}">
            <span data-feather="file"></span>Tools
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'intrusion-set'}}">
            <span data-feather="file"></span>Intrusion sets
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'vulnerability'}}">
            <span data-feather="file"></span>Vulnerabilities
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'campaign'}}">
            <span data-feather="file"></span>Campaigns
          </router-link>
        </li>
      </ul>

      <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
        <span>Observables</span>
        <a class="d-flex align-items-center text-muted" href="#">
          <span data-feather="plus-circle"></span>
        </a>
      </h6>
      <ul class="nav flex-column mb-2">
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'ObservableList'}">
            <span data-feather="home"></span>Browse observables
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'ObservablesBulk'}">
            <span data-feather="home"></span>Bulk observable match
          </router-link>
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

/*
 * Sidebar
 */

.sidebar {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 100; /* Behind the navbar */
  padding: 0;
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
}

.sidebar-sticky {
  position: -webkit-sticky;
  position: sticky;
  top: 48px; /* Height of navbar */
  height: calc(100vh - 48px);
  padding-top: .5rem;
  overflow-x: hidden;
  overflow-y: auto; /* Scrollable contents if viewport is shorter than content. */
}

.sidebar .nav-link {
  font-weight: 500;
  color: #333;
}

.sidebar .nav-link .feather {
  margin-right: 4px;
  color: #999;
}

.sidebar .nav-link.router-link-active {
  color: #007bff;
}

.sidebar .nav-link:hover .feather,
.sidebar .nav-link.router-link-active .feather {
  color: inherit;
}

.sidebar-heading {
  font-size: .75rem;
  text-transform: uppercase;
}

</style>
