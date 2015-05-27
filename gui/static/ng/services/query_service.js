(function () {
    angular.module("neuralGuiApp.services")
        .factory("NeuralService", function ($resource) {
            return {
                query: $resource("http://" + window.location.hostname + ":" + (parseInt(location.port) + 1000).toString() + "/query", null, {
                    go: {method: "POST"}
                }),
                train: $resource("http://" + window.location.hostname + ":" + (parseInt(location.port) + 1000).toString() + "/train", null, {
                    go: {method: "POST"}
                })
            };


        });
})();