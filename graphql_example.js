socket.post("https://api.scaphold.io/graphql/shop-o-data")
.data({
    query: 'mutation CreateTrafficMut($input: _CreateTrafficInput!) {
      createTraffic(input: $input) {
        changedTraffic {
          id
          sensor {
            id
            location
          }
          createdAt
        }
      }
    }',
    variables: {
        input: {
            'sensorId': ....,
            
        }
    }

})