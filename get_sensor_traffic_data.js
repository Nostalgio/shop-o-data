"https://api.scaphold.io/graphql/<api_key>?query={viewer{allSensors{edges{node{id traffic_data { edges { node {  createdAt } } } } } } } }"
{ 
    viewer { 
        allSensors {
            edges { 
                node {
                    id 
                    traffic_data { 
                        edges { 
                            node { 
                                createdAt 
                            }
                        }
                    }
                }
            }
        }
    }
}