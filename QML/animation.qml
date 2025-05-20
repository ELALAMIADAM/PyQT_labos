import QtQuick 2.5
import QtQuick.Controls 1.4

ApplicationWindow {
    visible: true
//    x:300
//    y:500
    width: 600
    height: 500
    title: "Animation"

 Item {
    width: 100; height: 100
    Rectangle {
        width: 100; height: 100
        color: "red"
    
        PropertyAnimation on x { to: 100; duration: 1000 }
        PropertyAnimation on y { to: 100; duration: 5000 }
    }
  }
}
