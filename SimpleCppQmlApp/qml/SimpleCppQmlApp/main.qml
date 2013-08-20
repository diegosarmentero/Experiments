import QtQuick 2.0

Rectangle {
    width: 360
    height: 360

    function change_color(color) {
        rect.color = color;
    }

    property alias opacidad: rect.opacity

    Rectangle {
        id: rect
        anchors.fill: parent
        anchors.margins: 100
        color: "blue"

        Text {
            text: qsTr("Hello World")
            anchors.centerIn: parent
            color: "white"
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            cppObject.funcionCpp("Click in qml");
        }
    }
}
