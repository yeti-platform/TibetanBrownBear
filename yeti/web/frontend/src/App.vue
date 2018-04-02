<template>

  <div id="app">

    <!-- Top menu -->
    <navigation/>

    <div class="container-fluid">
      <div class="row">
        <!-- sidebar column -->
        <sidebar/>
        <main role="main" class="col-md-9 ml-sm-auto col-lg-10 pt-3 px-4">
          <router-view/>
        </main>

      </div> <!-- end row -->
    </div>

  </div>

</template>

<script>
import Sidebar from '@/components/scaffolding/Sidebar'
import Navigation from '@/components/scaffolding/Navigation'

require('bootstrap')
require('bootstrap/dist/css/bootstrap.css')

export default {
  components: {
    Sidebar,
    Navigation
  },
  name: 'App',
  metaInfo: {
    title: 'Yeti',
    titleTempalte: 'Yeti | %s',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1, shrink-to-fit=no' }
    ]
  }
}
</script>

<style>
body {
  font-size: .875rem;
}

.feather {
  width: 16px;
  height: 16px;
  vertical-align: text-bottom;
}

.border-top { border-top: 1px solid #e5e5e5; }
.border-bottom { border-bottom: 1px solid #e5e5e5; }

</style>
