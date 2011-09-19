#ifndef RANGE_COMPRESS_H
#define RANGE_COMPRESS_H

struct range_request;
struct range;

const char* do_range_compress(struct range_request* rr, const struct range* r);

#endif /* RANGE_COMPRESS_H */
