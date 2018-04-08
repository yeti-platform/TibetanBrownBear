// scaffolding
import TableFilter from '@/components/scaffolding/TableFilter'
import YetiForm from '@/components/scaffolding/YetiForm'

export function generateRoutes (subComponents, defaults) {
  let defaultApiPath = defaults.defaultApiPath
  let defaultTypePrefix = defaults.defaultTypePrefix
  let defaultQuerykey = defaults.defaultQuerykey

  let generatedChildrenRoutes = []
  subComponents.map(subcompDefinition => {
    let apiPath = subcompDefinition.apiPath ? subcompDefinition.apiPath : defaultApiPath
    let queryKey = subcompDefinition.Querykey ? subcompDefinition.Querykey : defaultQuerykey
    let type = subcompDefinition.typePrefix ? subcompDefinition.typePrefix + subcompDefinition.name : defaultTypePrefix + subcompDefinition.name

    // push main view for route
    generatedChildrenRoutes.push({
      path: subcompDefinition.name,
      component: TableFilter,
      props: {
        apiPath: apiPath,
        querykey: queryKey,
        fields: subcompDefinition.fields,
        typeFilter: type
      }
    })

    // push edit / add view for route
    generatedChildrenRoutes.push({
      path: subcompDefinition.name + '/new',
      component: YetiForm,
      props: {
        apiPath: apiPath,
        fields: subcompDefinition.fields,
        type: type
      }
    })
  })

  // return the final generated route list
  return generatedChildrenRoutes
}
