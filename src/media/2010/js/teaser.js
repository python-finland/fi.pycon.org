//RGB values for sky colours. It would be nicer to pull these values from the CSS classes, but...
var night   = [126, 130, 140],
    dawn    = [100, 163, 184],
    glare   = [255, 255, 255],
    day     = [137, 213, 240],
    sunset  = [255, 220, 136],
    dusk    = [215, 148, 70];

//Color-stops that are applied according to the sun's travel through its arc
var skyPoints = [
    { pos: 0.0,   color: night  },
    { pos: 0.25,  color: dawn   },
    { pos: 0.29,  color: day    },
    //{ pos: 0.31,  color: glare  },
    { pos: 0.33,  color: day    },
    { pos: 0.6,   color: day    },
    { pos: 0.7,   color: sunset },
    { pos: 0.85,  color: dusk   },
    { pos: 0.9,   color: night  }
];

var spinRate = 1.5; //how fast the sun should spin

var SECOND  = 1000,
    MINUTE  = 60*SECOND,
    HOUR    = 60*MINUTE,
    DAY     = 24*HOUR;

var d=document, g="getElementById",
    arc = d[g]("arc"),
    sun = d[g]("sun"),
    sky = d[g]("sky"),
    masthead = d[g]("masthead");

function rotate()
{
    var time = new Date();
    
    //Current milliseconds from Epoch with offset
    var ms = time.getTime() + timeOffset;

    //how far we are through a complete rotation
    var sunPosition = (ms % rotationTime) / rotationTime;
    
    rotateTo(sunPosition);
}

function rotateTo(sunPosition)
{   
    //the angle of the sun's elevation in radians, reversed so that we go clockwise
    var elevation = -(sunPosition * 2 * Math.PI);
    
    //convert elevation to x, y coordinates (from -1 to 1)
    var x = Math.sin(elevation),
        y = Math.cos(elevation);
    
    //map coordinates to CSS offsets (from 0 to 100%)
    var s=sun.style;
    s.left  = ((x + 1) * 50) + "%";
    s.top   = ((y + 1) * 50) + "%";
    
    var sunAngle = (elevation * spinRate) * (180 / Math.PI);
    
    //extra shiny for webkit, Firefox 3.1+ and Opera 10.5: rotate the sun as we go
    s['-webkit-transform'] = s['MozTransform'] = s['-o-transform'] = "rotate(" + sunAngle + "deg)";

    applySkyColor(sunPosition);
}

//Set the appropriate sky colour based on the sun's position. Smoothly interpolates between one sky colour and the next.
function applySkyColor(sunPosition)
{
    var i, from, to;
    
    //Figure out our position in the color list based on the sun's position
    for (i=skyPoints.length-1; i>=0; i--)
    {
        if (i==0 || sunPosition > skyPoints[i].pos)
        {
            from = skyPoints[i];
            to   = skyPoints[i+1];
            break;
        }
    }

    if (to && to.color != from.color)
    {
        var ratio       = getRatio(from.pos, to.pos, sunPosition);
        var skyColor    = interpolateColor(from.color, to.color, ratio);
    }
    else skyColor = from.color;
    
    sky.style.backgroundColor = "rgb(" + skyColor.join(",") + ")";
    masthead.style.color = sky.style.backgroundColor;
}

//Linearly interpolate two values
function getRatio(from, to, current)    { return (current - from) / (to - from); }
function interpolate(from, to, ratio)   { return ((to - from) * ratio) + from; }
function interpolateColor(from, to, ratio)
{
    var i, final = [];
    for (i=0; i<3; i++) final[i] = interpolate(from[i], to[i], ratio).toFixed();
    return final;
}

/* Actual masthead animations */
/* -------------------------- */

var rotateAnimation = {
    startPos:   0.15,   //start a little before dawn
    endPos:     0.9,    //end at just after dusk
    
    frameRate:  SECOND/40,      //how fast we should animate the movement
    rotationTime: 30*SECOND,    //how long a full rotation should take
    
    start: function()
    {
        var t=this;
        t.startTime = new Date().getTime();
        t.timer     = setInterval(function(){ t.doFrame() }, t.frameRate);
        t.doFrame();
    },
    end: function()
    {
        clearInterval(this.timer);
        this.timer=null;        
    },
    doFrame: function()
    {
        var elapsedTime = new Date().getTime() - this.startTime;
        var pos = (elapsedTime % this.rotationTime) / this.rotationTime;
        pos += this.startPos;
        
        if (pos > this.endPos) this.end();
        else rotateTo(pos);
    }
};

rotateAnimation.start();