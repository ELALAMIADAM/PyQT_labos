#include "toplevel.h"

Toplevel::Toplevel(QWidget* parent):QDialog(parent){
  this->setWindowTitle("CAI : Dialog Window");
  QVBoxLayout *layout= new QVBoxLayout();
  QLabel *image= new QLabel(this);
//  QResource::registerResource("helloworld.qrc");
  image->setPixmap(QPixmap("Images/pyqt.jpg"));
  QPushButton *button= new QPushButton("Hide me !", this);
  QWidget::connect(button,SIGNAL(clicked()),this,SLOT(hide()));
  layout->addWidget(image);
  layout->addWidget(button);
  this->setLayout(layout);
}
