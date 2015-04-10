(function () {
    angular.module("neuralGuiApp.services")
        .factory("NeuralService", function ($resource) {
            return $resource("/query", null, {
                $query: {method: "POST"}
            });
        });
})();