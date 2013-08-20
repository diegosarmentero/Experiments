// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Rectangle {
    id: game
    width: 800
    height: 600
    color: "light blue"

    Rectangle {
        id: floor
        height: 50
        width: parent.width
        x: 0
        y: parent.height - 50
        color: "#95671e"
    }

    Sprite {
        id: guybrush
        x:50
        y: parent.height - 150 - floor.height
        width: 104;height: 150
        source: "./images/gb_walk.png"
        running: true
        frameCount: 6
    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            var pos = mouseX - (guybrush.width / 2);
            var posY = mouseY - guybrush.height;
            var difference = Math.abs(guybrush.x - pos);
            var duration = difference * 1000 / 100;
            guybrush.duration = duration;
            if(mouseX < guybrush.x){
                guybrush.state = "left";
                guybrush.x = pos;
            }else{
                guybrush.state = "right";
                guybrush.x = pos;
            }
            if(posY > 0){
                guybrush.y = posY;
                guybrush.scale = 0.5;
            }
        }
    }
}
