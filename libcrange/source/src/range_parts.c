#include <assert.h>
#include <string.h>
#include <pcre.h>
#include "range_parts.h"
#include <apr_strings.h>

static pcre* num_node_re = 0;

node_parts_int* node_to_parts(apr_pool_t* pool, const char* node_name)
{
    const char* buf[3];
    int offsets[20];
    int count;
    node_parts_int* result = apr_palloc(pool, sizeof(node_parts_int));
    result->full_name = node_name;
    count = pcre_exec(num_node_re, NULL, node_name, strlen(node_name),
                      0, 0, offsets, 20);
    if (count > 0) {
        int i;
        for (i=1; i<count; ++i)
            pcre_get_substring(node_name, offsets, count, i, &buf[i-1]);
        result->prefix = apr_pstrdup(pool, buf[0]);
        result->num_str = apr_pstrdup(pool, buf[1]);
        result->num = atoi(buf[1]);
        result->domain = count > 3 ? apr_pstrdup(pool, buf[2]) : "";
        for (i=1; i<count; ++i) pcre_free_substring(buf[i-1]);
    }
    else {
        result->prefix = "";
        result->domain = "";
        result->num = 0;
    }
    return result;
}

void init_range_parts(void)
{
    if (!num_node_re) {
        int offsets[20];
        const char* error;
        num_node_re = pcre_compile(NUMBERED_NODE_RE, 0, &error, offsets, NULL);
    }
    assert(num_node_re);
}
