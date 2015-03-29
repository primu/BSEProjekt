(function () {
    angular.module("neuralGuiApp.controllers")
        .controller("DemoCtrl", function ($scope, $timeout) {

            $scope.history = [
                {
                    "item": "a",
                    "recognizedLetter": "A"
                }
            ];

        }).config(function ($mdThemingProvider) {
            $mdThemingProvider.theme('default')
                .primaryPalette('pink')
                .accentPalette('orange');
        });
})();