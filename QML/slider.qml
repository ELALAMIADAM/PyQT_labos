import QtQuick 2.5
import QtQuick.Controls 1.4

ApplicationWindow {
    visible: true
    id: rootwin
    width: 300
    height: 200
    title: "Slider"
    Row {
        Slider {
            id: slider
            minimumValue: 0
            maximumValue: 100
        }
        
        Label {
            text: Math.floor(slider.value)
        }            
    }
}
