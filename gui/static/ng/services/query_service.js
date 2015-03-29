(function () {
    angular.module("neuralGuiApp.services")
        .factory("", function ($resource) {
            return $resource("/save", null, {
                $save: {method: "POST"}
            });
        });
})();