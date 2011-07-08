#ifndef AST_H
#define AST_H

#include "libcrange.h"
#include "range.h"

typedef enum {
    AST_LITERAL,
    AST_NONRANGE_LITERAL,
    AST_UNION,
    AST_GROUP,
    AST_BRACES,
    AST_DIFF,
    AST_INTER,
    AST_NOT,
    AST_REGEX,
    AST_PARTS,
    AST_FUNCTION,
    AST_NOTHING
} rangetype;

typedef struct rangeast
{
    rangetype type;
    union
    {
        char *string;
        rangeparts *parts;
    } data;
    
    struct rangeast *children;
    struct rangeast *next;
} rangeast;

rangeast* range_ast_new(apr_pool_t* pool, rangetype type);
range* range_evaluate(range_request* rr, const rangeast* ast);

#endif
