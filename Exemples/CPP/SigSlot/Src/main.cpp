#include <QDebug>
#include <QPushButton>
#include <sigslot.h>

int main(int argc, char* argv[]) {
SigSlot a, b;

QObject::connect(&a, SIGNAL(valueChanged(int)), &b, SLOT(setValue(int)));
// QObject::connect(&b, SIGNAL(valueChanged(int)), &a, SLOT(setValue(int)));
b.setValue( 10 );
qDebug() << a.getValue(); // 0 or 10 ?
a.setValue( 100 );
qDebug() << b.getValue(); // 10 or 100 ?
} 

