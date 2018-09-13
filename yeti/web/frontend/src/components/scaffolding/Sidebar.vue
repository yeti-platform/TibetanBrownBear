<template lang="html">
  <nav class="col-md-2 d-none d-md-block bg-light sidebar">
    <div class="sidebar-sticky">
      <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
        <span>Intelligence</span>
      </h6>
      <ul class="nav flex-column">
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'attack-pattern'}}">
            <i class="fas fa-fw fa-lg fa-gamepad"></i>Attack Patterns (TTPs)
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'campaign'}}">
            <i class="fas fa-fw fa-lg fa-fighter-jet"></i>Campaigns
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'course-of-action'}}">
            <i class="fas fa-fw fa-lg fa-medkit"></i>Courses of action
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'identity'}}">
            <i class="fas fa-fw fa-lg fa-id-card"></i>Identities
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'intrusion-set'}}">
          <i class="fas fa-fw fa-lg fa-umbrella"></i>Intrusion sets
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'malware'}}">
            <i class="fas fa-fw fa-lg fa-bug"></i>Malware
          </router-link>
        </li>
         <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'report'}}">
            <i class="far fa-fw fa-lg fa-newspaper"></i>Reports
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'threat-actor'}}">
            <i class="fas fa-fw fa-lg fa-user-secret"></i>Threat actors
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'tool'}}">
            <i class="fas fa-fw fa-lg fa-wrench"></i>Tools
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'EntityList', params: {type: 'vulnerability'}}">
            <i class="fas fa-fw fa-lg fa-bolt"></i>Vulnerabilities
          </router-link>
        </li>
      </ul>

      <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
        <span>Observables</span>
      </h6>
      <ul class="nav flex-column mb-2">
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'ObservableList'}">
            <i class="fas fa-fw fa-lg fa-search"></i>Browse observables
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'ObservablesBulk'}">
            <i class="fas fa-fw fa-lg fa-archive"></i>Bulk observable match
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

a svg {
  margin-right: 5px;
}

</style>
