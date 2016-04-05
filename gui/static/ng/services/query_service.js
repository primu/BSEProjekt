(function () {
    angular.module("neuralGuiApp.services")
        .factory("NeuralService", function ($resource) {
            return {
                query: $resource("http://" + window.location.hostname + ":10240/query", null, {
                    go: {method: "POST"}
                }),
                train: $resource("http://" + window.location.hostname + ":10240/train", null, {
                    go: {method: "POST"}
                })
            };


        });
})();