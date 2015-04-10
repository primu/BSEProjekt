(function () {
    angular.module("neuralGuiApp.directives")
        .directive("drawing", function (lodash) {
            "use strict";
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
                    ctx.lineWidth = 4;

                    function deflateArray(array, width, height) {
                        // convert vector to width x height matrix
                        var out = new Array(height);
                        var x = 0;
                        var y = 0;
                        out[0] = new Array(width);
                        for (var i = 0; i < array.length; i++) {
                            if (x == width) {
                                x = 0;
                                y += 1;

                                out[y] = new Array(width);
                            }
                            out[y][x] = array[i];
                            x++;
                        }

                        return out;
                    }

                    function flattenArray(array) {
                        var out = [];
                        for (var x = 0; x < array.length; x++) {
                            for (var y = 0; y < array[x].length; y++) {
                                out.push(array[x][y]);
                            }
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

                    function scaleTo(array, width, height) {
                        var originalX = array.length;
                        var originalY = array[0].length;

                        var scaleX = width / originalX;
                        var scaleY = height / originalY;

                        var out = new Array(width);
                        for (var i = 0; i < height; i++) {
                            out[i] = new Array(height);
                            for (var j = 0; j < height; j++) {
                                out[i][j] = 0;
                            }
                        }

                        for (var x = 0; x < array.length; x++) {
                            for (var y = 0; y < array[x].length; y++) {
                                var newX = parseInt(x * scaleX);
                                var newY = parseInt(y * scaleY);

                                if (out[newX][newY] == 0) {
                                    out[newX][newY] = array[x][y];
                                }
                            }
                        }

                        return out;
                    }

                    function setArray(imageData) {
                        imageData = JSON.parse(imageData);
                        imageData = scaleTo(imageData, canvasWidth, canvasHeight);
                        imageData = flattenArray(imageData);
                        var count = canvasWidth * canvasHeight;
                        count <<= 2;
                        var input = ctx.createImageData(canvasWidth, canvasHeight);

                        for (var i = 0; i < count; i++) {
                            input.data[i] = 0;
                        }

                        var idx = 0;
                        for (var i = 3; i < count; i += 4) {
                            input.data[i] = imageData[idx++];
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

                        scope.$on("getCanvasData", function (event, msg) {
                            if (!lodash.isUndefined(msg) && !lodash.isUndefined(msg.id) && msg.id == id) {
                                scope.$broadcast("canvasData", {
                                    id: id,
                                    matrix: getArray()
                                });
                            }
                        });
                    }
                }
            };
        });
})();