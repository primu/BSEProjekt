(function () {
    angular.module("neuralGuiApp.directives")
        .directive("drawing", function (lodash) {
            return {
                restrict: "A",
                link: function (scope, element, attrs) {

                    var id = attrs.drawingId || null;
                    var xSize = attrs.xSize || 16;
                    var ySize = attrs.ySize || 16;

                    var ctx = element[0].getContext('2d');
                    var canvas = element[0];

                    var canvasWidth = canvas.width;
                    var canvasHeight = canvas.height;

                    var xScale = xSize / canvasWidth;
                    var yScale = ySize / canvasHeight;

                    ctx.strokeStyle = "#000";
                    ctx.lineJoin = "round";
                    ctx.lineWidth = 2;

                    function deflateArray(array, width, height) {
                        var out = new Array(height);
                        var x = 0;
                        var y = 0;

                        for (var i = 0; i < array.length; i++) {
                            if (x > width) {
                                x = 0;
                                y += 1;

                                out[y] = new Array(width);
                            }
                            out[y][x] = array[i];
                            x++;
                        }

                        return out;
                    }

                    function getArray() {
                        var imageData = ctx.getImageData(0, 0, canvasWidth, canvasHeight).data;
                        var count = canvasWidth * canvasHeight;
                        var out = new Array(count);
                        count <<= 2;
                        var idx = 0;
                        for (var i = 3; i < count; i += 4) {
                            out[idx++] = imageData[i];
                        }
                        return deflateArray(out, canvasWidth, canvasHeight);
                    }

                    function setArray(imageData) {
                        var count = imageData.length << 2;
                        var input = new Array(count);

                        lodash.fill(input, 0);
                        var idx = 0;
                        for (var i = 3; i < count; i += 4) {
                            input[i] = imageData[idx++];
                        }
                        ctx.putImageData(input, 0, 0);
                    }

                    if (!lodash.isUndefined(attrs.drawingMatrix)) {
                        setArray(attrs.drawingMatrix);
                    }

                    if (lodash.isUndefined(attrs.readonly) || attrs.readonly == false) {
                        // for non-readonly

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
                            // attrs.$set("matrix", getArray());
                            // scope.$apply();
                        });

                        function draw(lX, lY, cX, cY) {
                            ctx.moveTo(lX, lY);
                            ctx.lineTo(cX, cY);
                            ctx.stroke();
                        }

                        scope.$on("clearCanvas", function (event, msg) {
                            if (!lodash.isUndefined(msg) && !lodash.isUndefined(msg.id) && msg.id == id) {
                                ctx.clearRect(0, 0, canvasWidth, canvasHeight);
                            }
                        });
                    }
                }
            };
        });
})();