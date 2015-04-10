(function () {
    angular.module("neuralGuiApp.controllers")
        .controller("DemoCtrl", function ($scope, $timeout, NeuralService) {


            $scope.current = {};
            $scope.history = [
            ];


            $scope.getCanvasData = function(event, msg) {

                NeuralService.$query(msg.matrix, function(data) {
                    console.log(data);
                    $scope.history.push({
                    id: msg.id,
                    matrix: msg.matrix,
                    recognized: "A"
                });

                if ($scope.history.length > 3) {
                    $scope.history = $scope.history.slice(1, $scope.history.length + 1);
                }

                $scope.onClearCanvas();
                });
            };

            $scope.$on("canvasData", $scope.getCanvasData);
            $scope.onSendQuery = function () {
                $scope.$broadcast("getCanvasData", {
                    "id": "main"
                });
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