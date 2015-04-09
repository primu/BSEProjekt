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

            $scope.getCanvasData = function() {

            };

            $scope.onSendQuery = function () {

            };

            $scope.onClearCanvas = function() {
                $scope.$broadcast("clearCanvas", {
                    "id": "main"
                });
            };

        }).config(function ($mdThemingProvider) {
            $mdThemingProvider.theme('default')
                .primaryPalette('pink')
                .accentPalette('orange');
        });
})();