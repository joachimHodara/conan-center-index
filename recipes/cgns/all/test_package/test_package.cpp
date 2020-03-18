#include "cgnslib.h"

void main() {
  int index_file;
  if (cg_open("grid_c.cgns", CG_MODE_WRITE, &index_file))
    cg_error_exit();

  cg_close(index_file);
}