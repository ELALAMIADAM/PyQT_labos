#include <QtWidgets>

int main(int argc, char *argv[]){
  QApplication app(argc,argv);
  QWidget window;
  window.resize(200,100);
  window.setWindowTitle("CAI : Hello World");
  QPushButton *button= new QPushButton("Click To Join",&window);
  button->move(100,50);
  button->setStyleSheet("background-color:yellow;");
  window.show();
  return app.exec();
}
