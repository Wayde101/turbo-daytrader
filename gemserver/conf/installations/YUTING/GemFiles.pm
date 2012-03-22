package GemFiles;
use strict;
use FindBin qw/$Bin/;
use File::Compare;
use base 'Seco::Gemstone::BaseFiles';

sub setup {
    my $self = shift;
    # Arguments are 'name', 'constructor', 'installer', 'priority'
    # Higher priority items are installed first
    # Default installer name is 'name' replacing [.-] with _
    # Default constructor is GemConstructor


    # The next line can be commented to turn off manifest checking.
    $self->add('manifest', priority => 999, comparator => sub { 1 } );

   
    $self->add('services', constructor => 'Seco::Gemstone::MapConstructor');
    $self->add('inetd.conf', constructor => 'Seco::Gemstone::MapConstructor');
    $self->add('passwd', 
        priority => 9, 
        constructor => 'Seco::Gemstone::PasswdConstructor');
    $self->add('group', priority => 9);
    $self->add('hosts.allow');
    $self->add('hosts');
    $self->add('servicebuilder.conf');
    $self->add('nsswitch.conf');
    $self->add('protocols');
    $self->add('hosts.equiv');
    $self->add('shosts');
    $self->add('sudoers');
    $self->add('ntp.conf');
    $self->add('resolv.conf', comparator => sub { 1 });
    $self->add('dnscache.fwd', comparator => sub { 1 } );
    $self->add('rsyncd.conf');
    $self->add('rsyncd.secrets');
    $self->add('sources.list.literal');
    $self->add('sources.list');
    $self->add('i18n');
    $self->add('yum.conf');
    # HACK to support old versions of seco-gemstone
    if (-e "/usr/local/lib/perl5/site_perl/Seco/Gemstone/PackageConstructor.pm") {
        $self->add('dpkg-list', 
            priority => -1, # do this last
            constructor => 'Seco::Gemstone::PackageConstructor',
            comparator => sub { 1 });
    } else {
        $self->add('dpkg-list', comparator => sub { 1 });
    }
    $self->add('chkconfig-list', comparator => sub { 1 });
    $self->add('ssh_known_hosts');
    $self->add('ssh_known_hosts2');
    $self->add('ssh_config');
    $self->add('sshd_config');
    $self->add('shosts');
    $self->add('hosts.equiv');
    $self->add('timezone');
    $self->add('sysctl.conf');
    $self->add('crontab');
    $self->add('limits.conf');
    $self->add('syslog.conf');
    $self->add('logrotate_syslog');
    $self->add('logrotate.conf');
    $self->add('main.cf');
    $self->add('postfix.virtual');
    $self->add('postfix.canonical_recipient');
    $self->add('postfix.transport');
    $self->add('aliases');
    $self->add('gemstonehints');
    $self->add('pam-sshd');
    $self->add('pam-su');
    $self->add('pam-login');
    $self->add('pam-passwd');
    $self->add('pam-cron');
    $self->add('syslog-ng.conf');
    $self->add('dump');
    $self->add('exports');
    $self->add('verification', comparator => sub { 1 } );
    $self->add('httpd.conf');
    $self->add('rrd.httpd.conf');
    $self->add('bucketProxy.httpd.conf', comparator =>
		sub {return compare("$Bin/../out/bucketProxy.httpd.conf", "/etc/apache/httpd.conf")} );
    $self->add('deProxy.httpd.conf', comparator =>
		sub {return compare("$Bin/../out/deProxy.httpd.conf", "/etc/apache/httpd.conf")} );
    $self->add('requests');
    $self->add('issue');
    $self->add('auto.home');
    $self->add('auto.master');
    $self->add('eth-config');
    $self->add('rules.txt', comparator => sub { 1 } );
    $self->add('yst-ip-list');
    $self->add('iptables-blessed');
    $self->add('iptables-pre-blessed');
    $self->add('iptables-post-blessed');
    $self->add('iptables-modules');
    $self->add('ld.so.conf');
    $self->add('ospfd.conf');
    $self->add('zebra.conf');
    $self->add('readahead');
    $self->add('dns_multilog',comparator => sub { 1 } );
    $self->add('updatedb.conf');
    $self->add('prelink');
    $self->add('autofsck');
    $self->add('fsckoptions');
    $self->add('yuting_home_ssh_config',comparator => sub { 1 });
}

1;
