// scaffolding
import TableFilter from '@/components/scaffolding/TableFilter'
import YetiForm from '@/components/scaffolding/YetiForm'

export function generateRoutes (subComponents, defaults) {
  let defaultApiPath = defaults.apiPath
  let defaultTypePrefix = defaults.typePrefix
  let defaultQuerykey = defaults.querykey

  let generatedChildrenRoutes = []
  subComponents.map(subcompDefinition => {
    let filterEndpoint = subcompDefinition.apiPath ? subcompDefinition.apiPath : defaultApiPath + 'filter/'
    let newEndpoint = subcompDefinition.apiPath ? subcompDefinition.apiPath : defaultApiPath
    let queryKey = subcompDefinition.Querykey ? subcompDefinition.Querykey : defaultQuerykey
    let type = subcompDefinition.typePrefix ? subcompDefinition.typePrefix + subcompDefinition.name : defaultTypePrefix + subcompDefinition.name

    // push main view for route
    generatedChildrenRoutes.push({
      path: subcompDefinition.name,
      component: TableFilter,
      props: {
        apiPath: filterEndpoint,
        querykey: queryKey,
        fields: subcompDefinition.fields,
        typeFilter: type
      }
    })

    // push 'new' view for route
    generatedChildrenRoutes.push({
      path: subcompDefinition.name + '/new',
      component: YetiForm,
      props: {
        apiPath: newEndpoint,
        fields: subcompDefinition.fields,
        object: {'type': type},
        onSaveCallback: defaults.onSaveCallback
      }
    })
  })
  // return the final generated route list
  return generatedChildrenRoutes
}
