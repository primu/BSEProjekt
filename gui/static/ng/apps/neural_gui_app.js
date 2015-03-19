(function () {
    angular.module("neuralGuiApp",
        ["ngMaterial", "ngResource",
            "neuralGuiApp.services", "neuralGuiApp.directives", "neuralGuiApp.controllers"])
    .config(function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}');
    });
})();