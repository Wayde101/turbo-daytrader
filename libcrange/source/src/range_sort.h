#ifndef RANGE_SORT_H
#define RANGE_SORT_H

struct range;
struct range_request;

const char** do_range_sort(struct range_request* rr, const struct range *r);

#endif /* RANGE_SORT_H */
