(function () {

    function LeanDialogController($scope, $mdDialog, item, NeuralService) {
        $scope.item = item;
        $scope.data = {
            expected: "",
            hard: true
        };

        $scope.learn = function () {
            NeuralService.train.go({
                data: item.matrix,
                character: $scope.data.expected,
                hard: $scope.hard
            }, function (data) {

            });
        };
    }

    angular.module("neuralGuiApp.controllers")
        .controller("DemoCtrl", function ($scope, $timeout, NeuralService, $mdDialog) {


            $scope.current = {};
            $scope.history = [];
            $scope.details = {
                processing: false
            };

            $scope.learn = function (item) {
                $mdDialog.show({
                    controller: LeanDialogController,
                    templateUrl: "static/ng/views/LearnDialog.html",
                    locals: {
                        item: item
                    }

                }).then(function () {

                }, function () {

                });
            };

            $scope.redo = function (item) {
                $scope.getCanvasData(null, {
                    id: "",
                    matrix: item.matrix
                })
            };

            $scope.getCanvasData = function (event, msg) {
                $scope.details.processing = true;
                NeuralService.query.go(msg.matrix, function (data) {
                    $scope.details.processing = false;
                    console.log(data);
                    $scope.history.unshift({
                        id: msg.id,
                        matrix: msg.matrix,
                        recognized: data.best_guess
                    });

                    if ($scope.history.length > 5) {
                        $scope.history.splice(-1, 1);
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

            $scope.onClearCanvas = function () {
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