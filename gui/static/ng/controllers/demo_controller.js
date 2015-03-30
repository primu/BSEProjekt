(function () {
    angular.module("neuralGuiApp.controllers")
        .controller("DemoCtrl", function ($scope, $timeout) {


            $scope.current = {};

            $scope.history = [
                {
                    "item": "a",
                    "recognizedLetter": "A"
                }
            ];

            $scope.onSendQuery = function () {

            };

        }).config(function ($mdThemingProvider) {
            $mdThemingProvider.theme('default')
                .primaryPalette('pink')
                .accentPalette('orange');
        });
})();