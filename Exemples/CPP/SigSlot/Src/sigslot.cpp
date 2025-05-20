#include "sigslot.h"

void SigSlot::setValue( int v ) {
   if ( v != _value ) {
    _value = v;
    emit valueChanged(v);
  }
}

