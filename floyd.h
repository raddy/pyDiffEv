#ifndef _FLOYD_H
#define _FLOYD_H

#include <math.h>
#include <stdlib.h>
#include <algorithm>


static int* unique_indices(int num_unique, int list_len){
	unsigned char used_dexes[list_len];
	std::fill(used_dexes,used_dexes+list_len,0);
	int in,im;
	int * res = (int *)malloc(sizeof(int)*num_unique);
	
	im = 0;

	for (in = list_len - num_unique; in < list_len && im < num_unique; ++in) {
  		int r = rand() % (in + 1);
  		if (used_dexes[r])
    		r = in; /* use 'in' instead of the generated number */

  		res[im++] = r + 1; /* +1 since your range begins from 1 */
  		used_dexes[r] = 1;
	}
	return res;
}

#endif