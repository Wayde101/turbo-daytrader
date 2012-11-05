#!/usr/bin/perl

sub fib {
    return @_[0] < 2 ? @_[0] : fib(@_[0]-1) + fib(@_[0]-2)
}

# Subroutine f(n) handles the negative arguments: F(-n) = F(n)*(-1)^(n+1)
sub f {
    if (@_[0] < 0) {
        return @_[0] % 2 ? fib(-@_[0]) : -fib(-@_[0]);
    } else {
        return fib(@_[0]);
    }
}

# Subroutine fib_print(n) prints out nth Fibonacci number
sub fib_print {
	print @_[0], "th Fibonacci number is ", f(@_[0]), "\n";
}

# entry point: check the number of command line parameters and check that
# the first parameter is an integer, if either fails, report usage information 
if ( $#ARGV || int($ARGV[0]) ne $ARGV[0]) {
    die "Usage: perl ", $0, " <n>\n";
} else {
   fib_print($ARGV[0]);
}
