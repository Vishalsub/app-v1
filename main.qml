import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Effects

Window {
    width: 480
    height: 720
    visible: true
    title: "CEVA Logistics Launcher"
    color: "#00000000"

    // Backend checker properties
    property string status: backendChecker ? backendChecker.status : "Initializing..."
    property int robotCount: backendChecker ? backendChecker.robotCount : 0
    property int cameraCount: backendChecker ? backendChecker.cameraCount : 0
    property bool launchReady: backendChecker ? backendChecker.launchReady : false

    // Connect to backend checker signals
    Connections {
        target: backendChecker
        function onStatusChanged(message) {
            status = message
        }
        function onRobotsDetected(count) {
            robotCount = count
        }
        function onCamerasDetected(count) {
            cameraCount = count
        }
        function onLaunchReady(ready) {
            launchReady = ready
        }
    }

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#9ddaf5" }
            GradientStop { position: 1.0; color: "#214c9c" }
        }

        Rectangle {
            id: glassPanel
            width: 400
            height: 600
            anchors.centerIn: parent
            radius: 25
            color: Qt.rgba(1,1,1,0.08)
            border.color: Qt.rgba(1,1,1,0.2)
            border.width: 1

            // Frosted blur layer
            Rectangle {
                anchors.fill: parent
                radius: parent.radius
                color: "transparent"
                layer.enabled: true
                layer.effect: MultiEffect {
                    blurEnabled: true
                    blur: 0.18
                }
            }

            // === Company Logo (top) ===
            Image {
                id: companyLogo
                source: "file:///Users/vishal/Documents/Projects/log/asset/CEVA_Logo_Blue_HR.jpg"
                width: 240
                height: 100
                fillMode: Image.PreserveAspectFit
                anchors.top: parent.top
                anchors.topMargin: 30
                anchors.horizontalCenter: parent.horizontalCenter
                smooth: true
            }

            // === Status Panel ===
            Rectangle {
                id: statusPanel
                width: 320; height: 180
                radius: 25
                color: "#000000"
                border.color: "#1db9ff"
                border.width: 3
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: companyLogo.bottom
                anchors.topMargin: 40
                opacity: 0.0

                // Fade-in animation
                SequentialAnimation {
                    running: true
                    NumberAnimation { target: statusPanel; property: "opacity"; from: 0; to: 1; duration: 800 }
                    PauseAnimation { duration: 500 }
                    ScriptAction { script: welcomeTypeTimer.start() }
                }

                property string welcomeText1: "WELCOME"
                property string welcomeText2: "CEVA LOGISTICS"
                property string currentWelcome1: ""
                property string currentWelcome2: ""

                // Welcome text
                Text {
                    id: welcomeText1
                    text: statusPanel.currentWelcome1
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 20
                    font.family: "Orbitron"
                    font.pixelSize: 24
                    color: "#00ffff"
                    opacity: 0.9
                }

                Text {
                    id: welcomeText2
                    text: statusPanel.currentWelcome2
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 50
                    font.family: "Orbitron"
                    font.pixelSize: 22
                    color: "#ff6666"
                    opacity: 0.9
                }

                // Status text
                Text {
                    id: statusText
                    text: backendChecker ? backendChecker.status : "Initializing..."
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 85
                    font.family: "Arial"
                    font.pixelSize: 14
                    color: "#ffffff"
                    opacity: 0.8
                    wrapMode: Text.WordWrap
                    width: parent.width - 20
                    horizontalAlignment: Text.AlignHCenter
                }

                // Device counts
                Row {
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 15
                    spacing: 30

                    Text {
                        text: "🤖 " + (backendChecker ? backendChecker.robotCount : 0)
                        font.family: "Arial"
                        font.pixelSize: 16
                        color: "#00ff00"
                        opacity: 0.9
                    }

                    Text {
                        text: "📷 " + (backendChecker ? backendChecker.cameraCount : 0)
                        font.family: "Arial"
                        font.pixelSize: 16
                        color: "#00ff00"
                        opacity: 0.9
                    }
                }

                // Welcome typing animation
                Timer {
                    id: welcomeTypeTimer
                    interval: 80
                    repeat: true
                    running: false
                    onTriggered: {
                        if (statusPanel.currentWelcome1.length < statusPanel.welcomeText1.length) {
                            statusPanel.currentWelcome1 += statusPanel.welcomeText1[statusPanel.currentWelcome1.length]
                        } else if (statusPanel.currentWelcome2.length < statusPanel.welcomeText2.length) {
                            statusPanel.currentWelcome2 += statusPanel.welcomeText2[statusPanel.currentWelcome2.length]
                        } else {
                            stop()
                        }
                    }
                }

                // Loading spinner
                Rectangle {
                    id: spinner
                    width: 20
                    height: 20
                    radius: 10
                    color: "transparent"
                    border.color: "#00ffff"
                    border.width: 2
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.bottom: statusText.top
                    anchors.bottomMargin: 10
                    visible: !backendChecker || !backendChecker.launchReady

                    RotationAnimation on rotation {
                        loops: Animation.Infinite
                        duration: 1000
                        from: 0
                        to: 360
                        running: spinner.visible
                    }
                }
            }

            // === Launch Button (bottom) ===
            Rectangle {
                id: launchButton
                width: 200
                height: 70
                radius: 35
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 40
                color: (backendChecker && backendChecker.launchReady) ? 
                       Qt.rgba(0,255,255,0.4) : Qt.rgba(0.1,0.1,0.1,0.6)
                border.color: (backendChecker && backendChecker.launchReady) ? 
                             "#00FF00" : "#666666"
                border.width: 2

                layer.enabled: true
                layer.effect: MultiEffect {
                    shadowEnabled: true
                    shadowBlur: 1.0
                    shadowColor: (backendChecker && backendChecker.launchReady) ? 
                                 "#00FF00" : "#666666"
                }

                Text {
                    text: (backendChecker && backendChecker.launchReady) ? "Launch Dashboard" : "Initializing..."
                    anchors.centerIn: parent
                    color: (backendChecker && backendChecker.launchReady) ? "white" : "#888888"
                    font.bold: true
                    font.pixelSize: 18
                    font.family: "Arial"
                }

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    enabled: backendChecker && backendChecker.launchReady
                    onEntered: {
                        if (backendChecker && backendChecker.launchReady) {
                            launchButton.color = Qt.rgba(0,255,255,0.6)
                        }
                    }
                    onExited: {
                        if (backendChecker && backendChecker.launchReady) {
                            launchButton.color = Qt.rgba(0,255,255,0.4)
                        }
                    }
                    onClicked: {
                        if (backendChecker && backendChecker.launchReady) {
                            backendChecker.launchDashboard()
                        }
                    }
                }

                // Pulse animation when ready
                SequentialAnimation {
                    id: readyPulse
                    loops: Animation.Infinite
                    running: backendChecker && backendChecker.launchReady
                    NumberAnimation { 
                        target: launchButton; 
                        property: "scale"; 
                        from: 1.0; 
                        to: 1.05; 
                        duration: 1000; 
                        easing.type: Easing.InOutQuad 
                    }
                    NumberAnimation { 
                        target: launchButton; 
                        property: "scale"; 
                        from: 1.05; 
                        to: 1.0; 
                        duration: 1000; 
                        easing.type: Easing.InOutQuad 
                    }
                }
            }
        }
    }
}
