#include <QObject> 

class SigSlot : public QObject {
Q_OBJECT
  public:
    SigSlot(): _value(0) {}
    int  getValue() const { return _value; }
  public slots:
    void setValue( int );  
  signals:
    void valueChanged( int );
  private:
    int  _value;
};

