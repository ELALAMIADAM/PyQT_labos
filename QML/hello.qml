import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    x:300
    y:500
    width: 600
    height: 500
    title: "HelloApp"

    Text {
        anchors.centerIn: parent
        text: "Hello World"
        font.pixelSize: 24
    }

}