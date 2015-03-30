(function () {
    angular.module("neuralGuiApp.directives")
        .directive("drawing", function () {
            return {
                restrict: "A",
                link: function (scope, element, attrs) {

                    var ctx = element[0].getContext('2d');
                    var canvas = element[0].canvas;

                    ctx.strokeStyle = "#000";
                    ctx.lineJoin = "round";
                    ctx.lineWidth = 2;

                    var paint = false;
                    var lastX;
                    var lastY;

                    element.bind('mousedown', function (event) {
                        if (event.offsetX !== undefined) {
                            lastX = event.offsetX;
                            lastY = event.offsetY;
                        } else {
                            lastX = event.layerX - event.currentTarget.offsetLeft;
                            lastY = event.layerY - event.currentTarget.offsetTop;
                        }

                        ctx.beginPath();
                        paint = true;
                    });
                    element.bind('mousemove', function (event) {
                        if (paint) {
                            var currentX, currentY;
                            // get current mouse position
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
                        paint = false;
                    });

                    function getArray() {
                        var canvasWidth = canvas.width;
                        var canvasHeight = canvas.height;
                        var imageData = ctx.getImageData(0, 0, canvasWidth, canvasHeight).data;
                        var count = canvasWidth * canvasHeight;
                        var out = new Array(count);
                        count <<= 2;
                        var idx = 0;
                        for (var i = 3; i < count; i += 4) {
                            out[idx++] = imageData[i];
                        }
                        return out;
                    }

                    function reset() {
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                    }

                    function draw(lX, lY, cX, cY) {
                        ctx.moveTo(lX, lY);
                        ctx.lineTo(cX, cY);
                        ctx.stroke();
                    }
                }
            };
        });
})();