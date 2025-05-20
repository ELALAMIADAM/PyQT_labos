#include <QtWidgets>
#include <toplevel.h>

int main(int argc, char *argv[]){
  QApplication app(argc,argv);
  QWidget window;
  window.resize(200,100);
  window.setWindowTitle("CAI : Hello World");
  QPushButton *button= new QPushButton("Clcik To Join",&window);
  button->move(100,50);
  button->setStyleSheet("background-color:yellow;");
  
  Toplevel* top= new Toplevel(&window);
  QWidget::connect(button,SIGNAL(clicked()), top,SLOT(show()));
  
  window.show();
  return app.exec();
}
