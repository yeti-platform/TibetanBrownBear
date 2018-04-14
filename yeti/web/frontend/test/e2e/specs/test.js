// For authoring Nightwatch tests, see
// http://nightwatchjs.org/guide#usage

module.exports = {
  'default e2e tests': function (browser) {
    // automatically uses dev Server port from /config.index.js
    // default: http://localhost:8080
    // see nightwatch.conf.js
    const devServer = browser.globals.devServerURL

    const index = devServer + '/'

    browser
      .url(index)
      .waitForElementVisible('#app', 1000)
      .assert.containsText('span', 'INTELLIGENCE')
      .end()
  }
}
