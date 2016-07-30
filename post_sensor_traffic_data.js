/**
* Use this snippet with your favorite
* JavaScript client frameworks.
* Resource: https://api.jquery.com/jquery.post/
*/

const data = {
    query: 'mutation CreateTraffic($input: _CreateTrafficInput!) { createTraffic(input: $input) { changedTraffic { id sensor { id } createdAt } } } ',
    variables: {"input": {"sensorId": "NTk0ZTVlNzQtNDA1Mi00OWFjLWI0OTMtYmI0NmQ4YTFmMGZkOjAxMGQzOTYzLTZkMzItNDc0Ny04OWVmLTEwMWVkMTg4NmZiOQ=="}}
};

$.ajax({
    type: "POST",
    url: "https://api.scaphold.io/graphql/<api_key>",
    data: data,
    success: function(result) {
        console.log("That was easy!");
        return result;
    },
    error: function(xhr, ajaxOptions, error) {
        console.log("That didn't go so well.");
        return error;
    },
    dataType: 'json'
});