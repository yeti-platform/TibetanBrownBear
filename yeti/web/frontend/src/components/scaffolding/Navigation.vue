<template lang="html">
  <nav class="navbar navbar-expand-md navbar-dark sticky-top bg-dark flex-md-nowrap p-0">
    <a class="navbar-brand col-sm-3 col-md-2 mr-0" href="#">Yeti</a>
    <div class="navbar-collapse" id="navbarCollapse">
    <ul class="navbar-nav px-3 ml-auto">
      <li class="nav-item">
          <router-link class="nav-link active" :to="{name: 'AdminMain'}">Admin</router-link>
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

.navbar-brand {
  padding-top: .75rem;
  padding-bottom: .75rem;
  font-size: 1rem;
  background-color: rgba(0, 0, 0, .25);
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, .25);
}

.navbar .form-control {
  padding: .75rem 1rem;
  border-width: 0;
  border-radius: 0;
}

.form-control-dark {
  color: #fff;
  background-color: rgba(255, 255, 255, .1);
  border-color: rgba(255, 255, 255, .1);
}

.form-control-dark:focus {
  border-color: transparent;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, .25);
}

</style>
