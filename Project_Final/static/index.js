
var canvas = document.getElementById('canvas'), ctx = canvas.getContext("2d");
ctx.strokeStyle = "black";
ctx.lineJoin = "round";
ctx.lineWidth = 5;
ctx.filter = "blur(1px)";




const
relPos = pt => [pt.pageX - canvas.offsetLeft, pt.pageY - canvas.offsetTop],
drawStart = pt => { with(ctx) { beginPath(); moveTo.apply(ctx, pt); stroke(); }},
drawMove = pt => { with(ctx) { lineTo.apply(ctx, pt); stroke(); }},

pointerDown = e => drawStart(relPos(e.touches ? e.touches[0] : e)),
pointerMove = e => drawMove(relPos(e.touches ? e.touches[0] : e)),

draw = (method, move, stop) => e => {
    if(method=="add") pointerDown(e);
    canvas[method+"EventListener"](move, pointerMove);
    canvas[method+"EventListener"](stop, ctx.closePath);
};
canvas.addEventListener("mousedown", draw("add","mousemove","mouseup"));
canvas.addEventListener("touchstart", draw("add","touchmove","touchend"));
canvas.addEventListener("mouseup", draw("remove","mousemove","mouseup"));
canvas.addEventListener("touchend", draw("remove","touchmove","touchend"));

function clearcanvas()
{
    var canvas = document.getElementById('canvas'),
        ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

