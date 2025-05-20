import QtQuick 2.5
import QtQuick.Controls 1.4

ApplicationWindow {
    visible: true
    id: rootwin
    width: 300
    height: 200
    title: "CheckBox"
    
    function onChecked(checked) {
        if (checked) {
            rootwin.title = "CheckBox"
        } else {
            rootwin.title = " "
        }
    }
    
    CheckBox {
        x: 15
        y: 15
        text: "Show title"
        checked: true
        onClicked: rootwin.onChecked(checked)
    }
}