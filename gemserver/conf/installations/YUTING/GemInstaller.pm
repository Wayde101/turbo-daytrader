package GemInstaller;

use strict;
use Data::Dumper;  # for debug hash
use Seco::Gemstone::Utils qw/gem_copy gem_move read_file write_file write_template motd/;
use File::Compare;
use Seco::RunAs;

sub new {
    my $class = shift;
    return bless {}, $class;
}

sub prelink {
    my $self = shift;
    return unless -d "/etc/sysconfig";
    gem_copy("out/prelink", "/etc/sysconfig/prelink");
}

sub autofsck {
    my $self = shift;
    return unless -d "/etc/sysconfig";
    gem_copy("out/autofsck", "/etc/sysconfig/autofsck");
}

sub fsckoptions {
    my $self = shift;
    return unless -d "/etc/sysconfig";
    gem_copy("out/fsckoptions", "/fsckoptions");
}

sub readahead {
    my $self = shift;
    open my $fh, "<out/readahead" or do {
        warn "ERROR: Can't open readahead: $!\n";
        return;
    };
    while (<$fh>) {
        next if /^#/;
        my ($device, $readahead) = split;
        next unless -e $device;
        system("blockdev --setra $readahead $device");
        if ($?) {
            warn "readahead: $device to $readahead returned an error\n";
        }
    }
    close $fh;
}

sub verification {
    my $self = shift;
    open my $fh, "<out/verification" or do {
        warn "ERROR: can't open verification: $!\n";
        return;
    };
    while(<$fh>) {
        next if /^#/;
        s/#.*//; s/\s+$//;
        next unless $_;
        /^(force\s+)?symlink\s+(\S+)\s+(\S+)/ and do {
            my ($force, $new, $old) = ($1, $2, $3);
            unless (-l $new and readlink $new eq $old) {
                if ($force) {
                    rmdir $new if -d $new;
                    unlink $new if -e $new;
                }
                warn "WARN: verification: setting symlink $new -> $old\n";
                symlink $old, $new or warn
                  "WARN: verification: could not symlink $new -> $old\n";
            }
            next;
        };
        /^directory\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)/ and do {
            my ($dir, $mode, $user, $group) = ($1, $2, $3, $4);
            my $uid = (getpwnam($user))[2];
            my $gid = getgrnam($group);
            
            unless(-d $dir) {
                warn "WARN: verification: creating $dir\n";
                mkdir $dir or warn "WARN: verification: could not mkdir $dir\n";
            }
            
            my @stat = stat $dir;
            $mode = oct($mode);
            unless (($stat[2] & 07777) == $mode and
                   $stat[4] == $uid and
                   $stat[5] == $gid) {
                warn "WARN: verification: setting permissions on $dir\n";
                chmod $mode, $dir
                  or warn "WARN: verification: unable to chmod $mode $dir\n";
                chown $uid, $gid, $dir or warn
                  "WARN: verification: unable to chown $uid:$gid $dir\n";
            }
            next;
        };
        /^file\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)/ and do {
            my ($file, $mode, $user, $group) = ($1, $2, $3, $4);
            my $uid = (getpwnam($user))[2];
            my $gid = getgrnam($group);
            
            unless(-f $file) {
                warn "WARN: verification: creating $file\n";
                open my $f, ">>$file" or warn
                  "WARN: verification: could not touch $file\n";
                close $f;
            }
            
            my @stat = stat $file;
            $mode = oct($mode);
            unless(($stat[2] & 07777) == $mode and
                   $stat[4] == $uid and
                   $stat[5] == $gid) {
                warn "WARN: verification: setting permissions on $file\n";
                chmod $mode, $file
                  or warn "WARN: verification: unable to chmod $mode $file\n";
                chown $uid, $gid, $file or warn
                  "WARN: verification: unable to chown $uid:$gid $file\n";
            }
            next;
        };
        
        warn "WARN: verification: $_\n";
    }
}

sub eth_config {
    my $self = shift;
    
    return unless -s "out/eth-config";
    open my $fh, "<out/eth-config" or do {
        warn "ERROR: Can't open eth-config: $!\n";
        return;
    };
    my @lines = <$fh>;
    close $fh;
    
    my $cmd = <<"";
#!/bin/sh
#
PATH=/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/bin

    for (@lines) {
        $cmd .= "ethtool -s $_";
    }
    
    open my $ofh, ">/usr/local/sbin/gemstone-eth";
    print $ofh $cmd;
    close $ofh;
    
    chmod 0755, "/usr/local/sbin/gemstone-eth";
    system("/usr/local/sbin/gemstone-eth");
    
    if ($self->is_redhat) {
        print "DEBUG: TODO: Redhat not implemented\n";
    } else {
        unless (-e "/etc/rcS.d/S41gemstone") {
            symlink "/usr/local/sbin/gemstone-eth", "/etc/rcS.d/S41gemstone";
        }
    }
}

sub i18n {
    my $self = shift;
    gem_copy("out/i18n", "/etc/sysconfig/i18n");
}

sub yum_conf {
    my $self = shift;
    gem_copy("out/yum.conf", "/etc/yum.conf");
}

sub chkconfig_list {
    my $self = shift;
    if(open my $chkconfig, "<out/chkconfig-list") {
        while(<$chkconfig>) {
            chomp;
            next unless $_;
            my ($sv, $onoff, $levels) = split /\s+/;
            next unless($onoff eq 'on' or $onoff eq 'off');
            
            system(qq(/sbin/chkconfig --add $sv));
            if($onoff eq 'on') {
                my $lev = '';
                $lev = "--level $levels" if($levels);
                system(qq(/sbin/chkconfig $sv $lev $onoff));
            } elsif($onoff eq 'off') {
                system(qq(/sbin/chkconfig $sv $onoff));
            }
        }
        close $chkconfig;
    }
}

sub dpkg_list {
    my $self = shift;
    my $dpkg_parms = $self->get_parms("out/dpkg-list");
    if (-d "/etc/apt") {

	# source.list use ubuntu 's 
        #system(qq/ ulimit -t 300; apt-get -qq update/);
        #if ($self->is_redhat) {
        #    my @pkgs = $self->get_packages_to_install;
        #    for my $pkg (@pkgs) {
        #        system(" ulimit -t 300; apt-get -q -y install $pkg\n");
        #    }
        #} else { # debian
	#	 # <package_name> <install|hold|deinstall|purge>
     system(<<'');
ulimit -t 300
dpkg --set-selections < out/dpkg-list
apt-get -q -y dselect-upgrade
apt-get -q -y install

#        }
#        system(qq/ ulimit -t 300; apt-get -q update/);
#        system(qq/ ulimit -t 300; apt-get clean/);
    } elsif (-e "/etc/yum.conf") {
        print STDERR "INFO: updating packages using yum\n";
	if ( ! exists $dpkg_parms->{"update"} || $dpkg_parms->{"update"}=~m/[disabled|0]/g) {
        	print STDERR "INFO: Does not run any yum update\n";
	}
	if (exists $dpkg_parms->{"update"} && $dpkg_parms->{"update"} eq 'gaoyang') {
        	print STDERR "running gaoyang yum update\n";
        	system(qq/ ulimit -t 300; yum -y -e 1 -d 1 update /);
	}

        my $yum_usage = `yum -h`;
        if ($yum_usage =~ /process-selections/) {
            system("ulimit -t 300; yum -y -e 1 -d 1 process-selections out/dpkg-list");
        } else {
            chomp(my @pkgs = $self->get_packages_to_install);
            while (@pkgs) {
                my @install = splice(@pkgs,0,8);
                system("ulimit -t 300; yum -y -e 1 -d 1 install @install");
            }
            chomp(@pkgs = $self->get_packages_to_remove);
            for my $pkg (@pkgs) {
                system("ulimit -t 300; rpm -q $pkg && yum -y -e 1 -d 1 remove $pkg");
            }
        }
    } elsif ( -e "/etc/pacman.conf" ) {
	print STDERR "ArchLinux have no dpkg-list support now\n";
    } elsif ( -e "/etc/slackware-version" ) {
	print STDERR "Slackware have no dpkg-list support now\n"
    }
    return 1;
}

sub get_packages_to_remove {
    local @_;
    my $self = shift;
    my @lines = grep { !/^\s*$/ and !/^#/ } split("\n", read_file("out/dpkg-list"));
    my @pkgs = map { @_=split; $_[0] } 
        grep { @_=split; $_[1] and ( $_[1] eq "remove" or $_[1] eq "purge" ) } @lines;
    return @pkgs;
}

sub get_parms {
   my ($self,$file) = (shift,shift);
   if ( not -e $file ) {  return {} ;}
   local @_;
   my %parms;
   my @lines = grep { /^#/ and /\{/ and /\}/} split("\n", read_file($file));
   my @kvs;
   foreach (@lines) {
     if(/\{(.*)\}/g) {
       @kvs = split(',',$1);
       foreach (@kvs) {
          if (/\s*(.*?)\s*\=\s*(.*)/) {
		$parms{$1}=$2;
	  }}}}
   return \%parms;
}

sub get_packages_to_install {
    local @_;
    my $self = shift;
    my @lines = grep { !/^\s*$/ and !/^#/ } split("\n", read_file("out/dpkg-list"));
    my @pkgs = map { @_=split; $_[0] } 
        grep { @_=split; $_[1] and $_[1] eq "install" } @lines;
    return @pkgs;
}

sub daemontools_svscanboot {
    my $self = shift;
    mkdir "/service" unless -d "/service";
    mkdir "/etc/service" unless -d "/etc/service";
    gem_copy("out/daemontools_svscanboot", "/usr/bin/svscanboot");
}

sub yuting_home_ssh_config {
    my $self = shift;
    run {  gem_copy("out/yuting_home_ssh_config","/home/yuting/.ssh/config") } 
	as user => 'yuting', group => "yuting" ;
}

sub yuting_home_bashrc {
    my $self = shift;
    run {  gem_copy("out/yuting_home_bashrc","/home/yuting/.bashrc") } 
	as user => 'yuting', group => "yuting" ;
}

sub group {
    my $self = shift;
    gem_copy("out/group", "/etc/group");
}

sub hosts_allow {
    my $self = shift;
    gem_copy("out/hosts.allow", "/etc/hosts.allow");
    gem_copy("out/hosts.allow", "/var/spool/postfix/etc/hosts") if (-f "/var/spool/postfix/etc/hosts");
}


sub hosts {
    my $self = shift;
    gem_copy("out/hosts", "/etc/hosts");
    gem_copy("out/hosts", "/var/spool/postfix/etc/hosts") if (-f "/var/spool/postfix/etc/hosts");
}

sub hosts_equiv {
    my $self = shift;
    gem_copy("out/hosts.equiv", "/etc/hosts.equiv") and
    gem_copy("out/hosts.equiv", "/etc/shosts.equiv") and
    gem_copy("out/hosts.equiv", "/etc/ssh/shosts.equiv");
}

sub inetd_conf {
    my $self = shift;

    unless ($self->is_redhat) {
        unlink("/etc/inetd.conf") and
        gem_copy("out/inetd.conf", "/etc/inetd.conf") and
        $self->restart_inetd;
    }
    return 1;
}

sub ntp_conf {
    my $self = shift;
    gem_copy("out/ntp.conf", "/etc/ntp.conf") and
    $self->restart_ntpd;
}

sub nsswitch_conf {
    my $self = shift;
    gem_copy("out/nsswitch.conf", "/etc/nsswitch.conf");
    gem_copy("out/nsswitch.conf", "/var/spool/postfix/etc/nsswitch.conf") if (-f "/var/spool/postfix/etc/nsswitch.conf");
}

sub passwd {
    my $self = shift;
    gem_copy("out/passwd", "/etc/passwd");
    system("pwconv");
}

sub protocols {
    my $self = shift;
    gem_copy("out/protocols", "/etc/protocols");
}

sub resolv_conf {
    my $self = shift;
    gem_copy("out/resolv.conf", "/etc/resolv.conf");
    if (-d "/var/spool/postfix/etc") {
        return gem_copy("out/resolv.conf", "/var/spool/postfix/etc");
    }
    return 1;
}


sub dnscache_fwd {
    my $self = shift;
    my $AT = '/etc/service/dnscache/root/servers/@';
    my $FO = '/etc/service/dnscache/env/FORWARDONLY';
    unless (-e "$AT.orig") {
      gem_copy("$AT","$AT.orig");
    }
    gem_copy("out/dnscache.fwd", $AT);
    open(FO,">$FO");
    print FO  "1\n";
    close FO;
    system("svc -t /service/dnscache");
    return 1;
}

sub rsyncd_conf {
    my $self = shift;
    gem_copy("out/rsyncd.conf", "/etc/rsyncd.conf") and
    $self->restart_rsyncd;
}

sub rsyncd_secrets {
    my $self = shift;
    gem_copy("out/rsyncd.secrets", "/root/rsyncd.secrets") and
    chmod 0700, "/root/rsyncd.secrets";
}

sub services {
    my $self = shift;
    gem_copy("out/services", "/etc/services");
    $self->restart_inetd;
    return 1;
}

sub shosts {
    my $self = shift;
    gem_copy("out/shosts", "/root/.shosts") and
    chmod 0400, "/root/.shosts";
}


sub sudoers {
    my $self = shift;
    gem_copy("out/sudoers", "/etc/sudoers") and
    chmod 0440, "/etc/sudoers" and
    chown 0, 0, "/etc/sudoers";
}

sub ssh_known_hosts {
    my $self = shift;

    print "DEBUG: Attempting to hardlink first\n";
    unlink("/etc/ssh/ssh_known_hosts.ln");
    my $cmd = "ln -f out/ssh_known_hosts /etc/ssh/ssh_known_hosts.ln && mv /etc/ssh/ssh_known_hosts.ln /etc/ssh/ssh_known_hosts";
    my $i = system $cmd;
    
    if ($i == 0) {
      print "SUCCESS with %cmd\n";
      return;
    } else {
      print "Hardlink method failed.  Using copy method.\n";
    }

    gem_copy("out/ssh_known_hosts", "/etc/ssh/ssh_known_hosts");
}

sub ssh_known_hosts2 {
    my $self = shift;
    gem_copy("out/ssh_known_hosts2", "/etc/ssh/ssh_known_hosts2");
}

sub ssh_config {
    my $self = shift;
    gem_copy("out/ssh_config", "/etc/ssh/ssh_config");
}

sub sshd_config {
    my $self = shift;
    gem_copy("out/sshd_config", "/etc/ssh/sshd_config") and
    $self->restart_sshd;
}

sub timezone {
    my $self = shift;
    chmod 0755, "out/timezone" and
    system("out/timezone");
    return 1;
}

sub sysctl_conf {
    my $self = shift;
    gem_copy("out/sysctl.conf", "/etc/sysctl.conf") and
    system("/sbin/sysctl -p");
    return 1;
}

sub crontab {
    my $self = shift;
    gem_copy("out/crontab", "/etc/crontab");
}

sub limits_conf {
    my $self = shift;
    gem_copy("out/limits.conf", "/etc/security/limits.conf");
}

sub syslog_conf {
    my $self = shift;
    gem_copy("out/syslog.conf", "/etc/syslog.conf") and
    $self->restart_syslogd;
}

sub logrotate_syslog {
    my $self = shift;
    gem_copy("out/logrotate_syslog", "/etc/logrotate.d/syslog");
}

sub logrotate_conf {
    my $self = shift;
    gem_copy("out/logrotate.conf", "/etc/logrotate.conf") and
    write_file("/etc/cron.daily/logrotate", <<'');
#!/bin/sh
/usr/sbin/logrotate /etc/logrotate.conf

    chmod 0755, "/etc/cron.daily/logrotate";
}


sub main_cf {
    my $self = shift;
    write_template("/etc/postfix/main.cf", read_file("out/main.cf"));
}

sub postfix_virtual {
    my $self = shift;
    write_template("/etc/postfix/postfix.virtual", 
        read_file("out/postfix.virtual"));
}

sub postfix_canonical_recipient {
    my $self = shift;
    write_template("/etc/postfix/postfix.canonical_recipient", 
        read_file("out/postfix.canonical_recipient"));
}

sub postfix_transport {
    my $self = shift;
    write_template("/etc/postfix/postfix.transport", 
        read_file("out/postfix.transport"));
}

sub aliases {
    my $self = shift;
    write_template("/etc/aliases",read_file("out/aliases"));
    system("newaliases");
}

sub reload_www {
  # utility
  # If /www/conf/httpd.conf exists, and any mention of "webacl" is 
  # invoked, then /www/bin/apachectl restart.  Primarilly, RRD boxes for
  # this specific issue at the moment.  Later should be extended to grep
  # and restart the "standard" debian apache.  Or, perhaps, a transform
  # created giving the location of apachectl, and we just always
  # gratiutiously reload. 

  if ( -x "/www/bin/apachectl") {
    if ( -f "/www/conf/httpd.conf") { 
      my $conf = read_file("/www/conf/httpd.conf");
      if ($conf =~ m/webacl/g) {
         print "webacl file changed: Restarting with /www/bin/apachectl restart\n";
         system("/www/bin/apachectl restart");
      }
    }
  }
}

sub gemstonehints {
    my $self = shift;
    gem_copy("out/gemstonehints", "/etc/gemstonehints");
}

sub pam_su {
    my $self = shift;
    gem_copy("out/pam-su", "/etc/pam.d/su");
}

sub pam_cron {
    my $self = shift;
    gem_copy("out/pam-cron", "/etc/pam.d/cron");
}

sub pam_sshd {
    my $self = shift;
    gem_copy("out/pam-sshd", "/etc/pam.d/sshd");
}

sub pam_login {
    my $self = shift;
    gem_copy("out/pam-login", "/etc/pam.d/login");
}

sub pam_passwd {
    my $self = shift;
    gem_copy("out/pam-passwd", "/etc/pam.d/passwd");
}

sub syslog_ng_conf {
    my $self = shift;
    unlink("/etc/syslog-ng.conf") and
      warn "removed bogus /etc/syslog-ng.conf - - - use /etc/syslog-ng/syslog-ng.conf";
    gem_copy("out/syslog-ng.conf", "/etc/syslog-ng/syslog-ng.conf") and
    $self->restart_syslogng;
}

sub dump {
    my $self = shift;
    gem_copy("out/dump", "/etc/sysconfig/dump") and
    system("lkcd config");
    return 1;
}

sub exports {
    my $self = shift;
    gem_copy("out/exports", "/etc/exports") and
    system(qw{/usr/bin/exportfs -a -r -v});
    return 1;
}


sub auto_home {
    my $self = shift;
    gem_copy("out/auto.home", "/etc/auto.home");
    return 1;
}


sub auto_master {
    my $self = shift;
    gem_copy("out/auto.master", "/etc/auto.master");
    return 1;
}

sub updatedb_conf {
    my $self = shift;
    gem_copy("out/updatedb.conf", "/etc/updatedb.conf");
    return 1;
}


sub iptables_modules {
    my $self = shift;
    system("mkdir", "-p", "/etc/yst-ipt");
    gem_copy("out/iptables-modules", "/etc/yst-ipt/iptables-modules");
    $self->restart_iptables;
    return 1;
}

sub iptables_pre_blessed {
    my $self = shift;
    system("mkdir", "-p", "/etc/yst-ipt");
    gem_copy("out/iptables-pre-blessed", "/etc/yst-ipt/iptables-pre-blessed");
    $self->restart_iptables;
    return 1;
}

sub iptables_post_blessed {
    my $self = shift;
    system("mkdir", "-p", "/etc/yst-ipt");
    gem_copy("out/iptables-post-blessed", "/etc/yst-ipt/iptables-post-blessed");
    $self->restart_iptables;
    return 1;
}

sub iptables_blessed {
    my $self = shift;
    system("mkdir", "-p", "/etc/yst-ipt");
    gem_copy("out/iptables-blessed", "/etc/yst-ipt/iptables-blessed");
    $self->restart_iptables;
    return 1;
}

sub restart_iptables {
    system "/etc/init.d/yst-iptables restart";
}

sub httpd_conf {
    my $self = shift;
    # Only for RH 8.0 boxes for now
    if (-d "/etc/httpd") {
        gem_copy("out/httpd.conf", "/etc/httpd/conf/httpd.conf") and
        $self->restart_apache;
    }
    return 1;
}

sub rrd_httpd_conf {
    my $self = shift;
    # /www should be a symlink pointing to the right places.
    system("mkdir","-p","/www/conf") unless (-d "/www/conf");
    system("mv","/www/conf/httpd.conf","/www/conf/httpd.conf.prev") if (-e "/www/conf/httpd.conf");
    gem_copy("out/rrd.httpd.conf","/www/conf/httpd.conf");
    reload_www();
    return 1;
}

sub bucketProxy_httpd_conf {
	my $self = shift;
	system("mv","/etc/apache/httpd.conf", "/etc/apache/httpd.conf.old");
	gem_copy("out/bucketProxy.httpd.conf","/etc/apache/httpd.conf");
	reload_www();
	return 1;
}

sub deProxy_httpd_conf {
	my $self = shift;
	system("mv","/etc/apache/httpd.conf", "/etc/apache/httpd.conf.old");
        system("mkdir","-p","/export/crawlspace/apache/log");
	gem_copy("out/deProxy.httpd.conf","/etc/apache/httpd.conf");
	reload_www();
	return 1;
}

# Support routines

# TODO maybe use a Template system
sub is_redhat {
    my $self = shift;
    return -f "/etc/redhat-release";
}

sub restart_inetd {
    my $self = shift;
    return if $self->is_redhat;

    system("killall inetd"); # let supervise restart it
}

sub restart_ntpd {
    my $self = shift;
    if( -e "/service/ntpd ") {
        system("svc -t /service/ntpd");
    } elsif ( -x "/etc/init.d/ntpd" ) {
	system("nice -n -10 /etc/init.d/ntpd restart");
    } else {
        print STDERR "ERROR: Need to restart ntpd and don't know how.\n";
    }
}

sub restart_rsyncd {
    my $self = shift;
    system("svc -t /service/rsync");
}

sub restart_sshd {
    my $self = shift;
    if (-e "/service/sshd") {
        system("svc -t /service/sshd");
    } elsif (-x "/etc/init.d/sshd") {
        system("nice -n -10 /etc/init.d/sshd restart");
    } else {
        print STDERR "ERROR: Need to restart sshd and don't know how.\n";
    }
}

sub restart_syslogd {
    my $self = shift;
    if ($self->is_redhat) {
        system("killall -1 syslogd");
    } else {
        system("svc -h /service/syslogd");
    }
}

sub restart_syslogng {
    my $self = shift;
    system("killall syslog-ng");
}

sub restart_apache {
    my $self = shift;
    system("/etc/init.d/apache reload");
}

sub requests {
    my $self = shift;
    my $requests = read_file("out/requests");
    for ($requests) {
        s/^#.*//m;
        s/\s+//g;
    }

    motd("requests", "Please use $requests for requests regarding this machine.");
}

sub make_homedirs_linux_pl {
    my $self = shift;
    if ((-e "out/make-homedirs-linux.pl") && (-s "out/make-homedirs-linux.pl"))
    {
       print "Running out/make-homedirs-linux.pl\n";
       system("perl out/make-homedirs-linux.pl");
    } else {
       print "Missing out/make-homedirs-linux.pl\n";
    }
}


sub issue {
    my $self = shift;
    gem_copy("/etc/issue","/etc/issue.orig") unless (-e "/etc/issue.orig");
    system("cat out/issue /etc/issue.orig > /etc/issue");
}
sub yst_ip_list {
    my $self = shift;
    gem_copy("out/yst-ip-list","/etc/yst-ip-list");
}

sub rules_txt {
   my $self = shift;
   my @runs = glob("/service/*/run");
   my @runs_ruled;
   return unless @runs;
   foreach (@runs) {
     my $d = $_ ; $d =~ s#/run$##;
     my ($tcpserver,$x,$X,$rules,$changed) = (0,0,0,0,0);
     open my $fh,"<$_" or die "ERROR: Couldn't open $_: $!\n";
     while(my $line=<$fh>) {
       $line =~ s/#.*//;  # Remove comments before parsing this
       $tcpserver = 1 if ($line =~ /tcpserver/);
       $x         = 1 if ($line =~ /\s-x\s/);
       $X         = 1 if ($line =~ /\s-X\s/);
       $rules     = 1 if ($line =~ /\srules\.cdb\b/);
     }
     close $fh;

     if (($tcpserver) && (!$x) && (!$X) && (!$rules)) {
       print "DEBUG: file $_  tcpserver=$tcpserver x=$x X=$X rules=$rules\n";
       print "Adding rules.cdb support into $_\n";
       system("perl","-pi.bak","-e",'s/tcpserver /tcpserver -X -x rules.cdb /g',$_);
       ($tcpserver,$x,$X,$rules,$changed) = (1,1,1,1,1);
     }
     if ($rules) {
       # We are now looking at a directory name
       if (compare("out/rules.txt","$d/rules.txt")) {
         gem_copy("out/rules.txt","$d/rules.txt");
         $changed=1;
       } else {
         print "$_ no change for rules.txt\n";
       }
     }
     if ($changed) {
       local %ENV;$ENV{"PATH"} = "/bin:/usr/bin:/usr/local/bin";
       my $cmd = "cd $d && tcprules rules.cdb rules.tmp < rules.txt && svc -t .";
       print "% $cmd\n";
       system $cmd;
     }
   }
}

sub dns_multilog {
   my $self = shift;
   my @runs = glob("/service/*dns*/log/run");
   foreach (@runs) {
     my $d = $_;
     $d =~ s#/run##;

       # We are now looking at a directory name
       if (compare("out/dns_multilog","$d/run")) {
         gem_copy("out/dns_multilog","$d/run");
         print "restarting $d/.\n";
	 system("chmod 755 $d/run ; svc -t $d/.");
       } else {
         print "$_ no change for rules.txt\n";
       }
   }
}



sub servicebuilder_conf {
    gem_copy("out/servicebuilder.conf", "/etc/servicebuilder.conf");
}

sub ld_so_conf {
    gem_copy("out/ld.so.conf", "/etc/ld.so.conf");
    system("ldconfig");
}

sub ospfd_conf {
  my $self = shift;
  my $QUAGGA;

  if ($self->is_redhat) {
     $QUAGGA = "/etc/quagga";
  } else {
     $QUAGGA = "/export/crawlspace/quagga/etc";
  }
  if (! -d $QUAGGA) {
    warn "ospfd.conf can't be written, missing $QUAGGA";
    return;
  }
  write_template("$QUAGGA/ospfd.conf",read_file("out/ospfd.conf"));
  warn "NOT restarting ospfd automatically out of paranoia (sorry)\n";
}

sub zebra_conf {
  my $self = shift;
  my $QUAGGA;
  if ($self->is_redhat) {
     $QUAGGA = "/etc/quagga";
  } else {
     $QUAGGA = "/export/crawlspace/quagga/etc";
  }
  if (! -d $QUAGGA) {
    warn "zebra.conf can't be written, missing $QUAGGA";
    return;
  }
  write_template("$QUAGGA/zebra.conf",read_file("out/zebra.conf"));
  warn "NOT restarting zebra automatically out of paranoia (sorry)\n";
}

sub manifest {
  my $self = shift;  
  my @required = qw( ./.manifest.md5sum /usr/local/bin/verify-md5sum );
  my @missing = grep(! -f $_, @required);
  if (@missing) {
    warn "NOT checking manifest, missing @missing";
    return;
  }  
  system("/usr/local/bin/verify-md5sum . >/dev/null");
  if ($?) {
    die "Failed running /usr/local/bin/verify-md5sum . ; exit code $?";
  }
  warn "manifest: validated\n";
  return;
}

sub yuting_authorized_keys {
    my $self = shift;
    run {
	gem_copy("out/yuting_authorized_keys","/home/yuting/.ssh/authorized_keys");
	chmod 0644, "/home/yuting/.ssh/authorized_keys";
    } as user => 'yuting', group => "yuting" ;
}

1;
