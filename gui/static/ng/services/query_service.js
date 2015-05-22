(function () {
    angular.module("neuralGuiApp.services")
        .factory("NeuralService", function ($resource) {
            return $resource("http://" + window.location.hostname + ":10240/query", null, {
                $query: {method: "POST"}
            });
        });
})();