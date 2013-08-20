// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Item{
    id:sprite
    clip: true
    width: 104;height: 150
    property alias running: timer.running;
    property int frame:0
    property int frameCount: 0;
    property alias source: image.source
    property int duration: 2000;

    Image{
         id:image
         x:-sprite.width*sprite.frame
         y: 0
         smooth: true
     }

    Timer {
        id:timer
        interval: 200; running: false; repeat: true
        onTriggered: {
            nextFrame();
        }
    }

    // Animations
    Behavior on x { PropertyAnimation { duration: sprite.duration } }
    Behavior on y { PropertyAnimation { duration: sprite.duration } }
    Behavior on scale { PropertyAnimation { duration: sprite.duration } }

    states: [
        State {
            name: "left"
            PropertyChanges { target: rotation; angle: 180 }
        },
        State {
            name: "right"
            PropertyChanges { target: rotation; angle: 0 }
        }
    ]

    transform: Rotation {
        id: rotation
        origin.x: 50
        origin.y: 0
        axis.x: 0; axis.y: 1; axis.z: 0
        angle: 0
    }

    function nextFrame() {
        sprite.frame = ++sprite.frame  % sprite.frameCount
    }

}
