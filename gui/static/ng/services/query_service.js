(function () {
    angular.module("neuralGuiApp.services")
        .factory("NeuralService", function ($resource) {
            return $resource("http://ks390721.kimsufi.com:10240/query", null, {
                $query: {method: "POST"}
            });
        });
})();