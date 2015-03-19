(function () {
    angular.module("neuralGuiApp.directives")
        .directive("drawing", function () {
            return {
                restrict: "A",
                link: function (scope, element) {
                    var ctx = element[0].getContext('2d');
                    var drawing = false;

                    var lastX;
                    var lastY;

                    element.bind('mousedown', function (event) {
                        if (event.offsetX !== undefined) {
                            lastX = event.offsetX;
                            lastY = event.offsetY;
                        } else { // Firefox compatibility
                            lastX = event.layerX - event.currentTarget.offsetLeft;
                            lastY = event.layerY - event.currentTarget.offsetTop;
                        }

                        ctx.beginPath();

                        drawing = true;
                    });
                    element.bind('mousemove', function (event) {
                        if (drawing) {

                            if (event.offsetX !== undefined) {
                                currentX = event.offsetX;
                                currentY = event.offsetY;
                            } else {
                                currentX = event.layerX - event.currentTarget.offsetLeft;
                                currentY = event.layerY - event.currentTarget.offsetTop;
                            }

                            draw(lastX, lastY, currentX, currentY);

                            lastX = currentX;
                            lastY = currentY;
                        }

                    });
                    element.bind('mouseup', function (event) {
                        drawing = false;
                    });

                    // canvas reset
                    function reset() {
                        // element[0].width = element[0].width;
                    }

                    function draw(lX, lY, cX, cY) {
                        ctx.moveTo(lX, lY);
                        ctx.lineTo(cX, cY);
                        ctx.strokeStyle = "#000";
                        ctx.stroke();
                    }
                }
            };
        });
})();